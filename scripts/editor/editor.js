"use strict";

const state = { content: null, token: "", kind: "projects", selected: "", dirty: false, busy: false };
const byId = id => document.getElementById(id);

function node(tag, text = "", attrs = {}) {
  const item = document.createElement(tag);
  if (text) item.textContent = text;
  for (const [key, value] of Object.entries(attrs)) item.setAttribute(key, value);
  return item;
}

function status(message, error = false) {
  byId("status").textContent = message;
  byId("status").classList.toggle("error", error);
}

function dirty() {
  state.dirty = true;
  byId("saved-state").textContent = "Unsaved changes";
  byId("saved-state").classList.add("dirty");
}

function busy(value) {
  state.busy = value;
  for (const id of ["save", "build", "add-item", "import-word"]) byId(id).disabled = value;
  byId("editor-fields").disabled = value;
}

async function api(path, options = {}) {
  const response = await fetch(path, { ...options, headers: { "X-Editor-Token": state.token, ...options.headers } });
  const result = await response.json();
  if (!response.ok) throw new Error(result.error || "The request failed.");
  return result;
}

function entries() {
  return state.kind === "projects"
    ? Object.entries(state.content.projects).sort((a, b) => a[1].order - b[1].order || a[0].localeCompare(b[0]))
    : state.content.research.modules.map(item => [item.id, item]);
}

function current() {
  return state.kind === "projects" ? state.content.projects[state.selected] : state.content.research.modules.find(item => item.id === state.selected);
}

function field(label, value, onInput, options = {}) {
  const wrapper = node("label", "", { class: `field${options.full ? " full" : ""}` });
  wrapper.append(node("span", label, { class: "field-label" }));
  const input = node(options.textarea ? "textarea" : options.select ? "select" : "input");
  if (!options.textarea && !options.select) input.type = options.type || "text";
  if (options.select) {
    for (const [optionValue, optionText] of options.select) {
      const option = node("option", optionText);
      option.value = optionValue;
      input.append(option);
    }
  }
  input.value = value;
  if (options.required) input.required = true;
  if (options.maxLength) input.maxLength = options.maxLength;
  if (options.className) input.className = options.className;
  if (options.type === "number") { input.min = "1"; input.max = "1000"; input.step = "1"; }
  input.addEventListener(options.select ? "change" : "input", () => { onInput(input.value); dirty(); });
  wrapper.append(input);
  if (options.help) wrapper.append(node("span", options.help, { class: "field-help" }));
  return wrapper;
}

function button(text, handler, attrs = {}) {
  const item = node("button", text, { type: "button", ...attrs });
  item.addEventListener("click", handler);
  return item;
}

function renderList() {
  const list = byId("item-list");
  list.replaceChildren();
  for (const [key, item] of entries()) {
    const link = button(item.title, () => { state.selected = key; render(); }, { class: `item-link${key === state.selected ? " active" : ""}`, "aria-current": key === state.selected ? "true" : "false" });
    link.append(node("small", state.kind === "projects" ? `${item.featured ? "Featured · " : ""}${item.context}` : "Research direction"));
    list.append(link);
  }
  for (const kind of ["projects", "research"]) {
    const active = state.kind === kind;
    byId(`${kind}-tab`).classList.toggle("active", active);
    byId(`${kind}-tab`).setAttribute("aria-pressed", String(active));
  }
  byId("add-item").textContent = state.kind === "projects" ? "+ Add project" : "+ Add research direction";
}

function renderMetadata(item) {
  const metadata = byId("metadata");
  metadata.replaceChildren();
  metadata.append(field("Title", item.title, value => { item.title = value; byId("item-heading").textContent = value; }, { full: true, required: true, maxLength: 200 }));
  metadata.append(field("Summary", item.summary, value => item.summary = value, { full: true, textarea: true, required: state.kind === "projects", maxLength: 1500, help: "A brief introduction. Project summaries also appear in the project list and homepage highlights." }));
  if (state.kind === "projects") {
    metadata.append(field("Context", item.context, value => item.context = value, { maxLength: 200, help: "For example: Professional work · HawarIT Limited" }));
    metadata.append(field("Your role", item.role, value => item.role = value, { maxLength: 200 }));
    metadata.append(field("Display order", item.order, value => item.order = Number(value), { type: "number", required: true }));
    const check = node("label", "", { class: "field check-field" });
    const input = node("input", "", { type: "checkbox" });
    input.checked = item.featured;
    input.addEventListener("change", () => { item.featured = input.checked; dirty(); });
    check.append(input, node("span", "Feature on homepage"));
    metadata.append(check);
    metadata.append(field("Related research", item.research_anchor, value => item.research_anchor = value, { full: true, select: [["", "No related direction"], ...state.content.research.modules.map(module => [module.id, module.title])] }));
  } else {
    const move = node("div", "", { class: "block-actions full" });
    const index = state.content.research.modules.indexOf(item);
    const reposition = change => {
      const target = index + change;
      if (target < 0 || target >= state.content.research.modules.length) return;
      [state.content.research.modules[index], state.content.research.modules[target]] = [state.content.research.modules[target], state.content.research.modules[index]];
      dirty(); render();
    };
    const up = button("Move direction up", () => reposition(-1));
    const down = button("Move direction down", () => reposition(1));
    up.disabled = index === 0;
    down.disabled = index === state.content.research.modules.length - 1;
    move.append(up, down); metadata.append(move);
  }
  metadata.append(node("p", state.kind === "projects" ? `Page address: /portfolio/${state.selected}/` : `Section anchor: #${state.selected}`, { class: "field-help field full" }));
  const intro = byId("intro-field");
  intro.hidden = state.kind !== "research";
  intro.replaceChildren();
  if (state.kind === "research") {
    const box = node("div", "", { class: "intro-box" });
    box.append(field("Research page introduction", state.content.research.introduction, value => state.content.research.introduction = value, { textarea: true, required: true, help: "Shared introduction above all research directions. Markdown is supported." }));
    intro.append(box);
  }
}

function renderBlocks(item) {
  const container = byId("blocks");
  container.replaceChildren();
  if (!item.blocks.length) container.append(node("p", "Add a text block or image block to start this page.", { class: "empty-blocks" }));
  item.blocks.forEach((block, index) => {
    const card = node("section", "", { class: "block-card", "aria-label": `Block ${index + 1}: ${block.type}` });
    const header = node("header");
    header.append(node("strong", `${index + 1}. ${block.type === "text" ? "Text" : "Image"} block`));
    const controls = node("div", "", { class: "move-buttons" });
    const move = change => {
      const target = index + change;
      if (target < 0 || target >= item.blocks.length) return;
      [item.blocks[index], item.blocks[target]] = [item.blocks[target], item.blocks[index]];
      dirty(); renderBlocks(item);
    };
    const up = button("↑", () => move(-1), { "aria-label": `Move block ${index + 1} up` });
    const down = button("↓", () => move(1), { "aria-label": `Move block ${index + 1} down` });
    up.disabled = index === 0; down.disabled = index === item.blocks.length - 1;
    controls.append(up, down, button("Remove", () => {
      if (!confirm("Remove this block? Unsaved changes can be discarded by reloading the editor.")) return;
      item.blocks.splice(index, 1); dirty(); renderBlocks(item);
    }));
    header.append(controls); card.append(header);
    if (block.type === "text") {
      card.append(field("Heading (optional)", block.heading, value => block.heading = value, { maxLength: 200 }));
      card.append(field("Text", block.body, value => block.body = value, { textarea: true, className: "text-body", help: "Use Markdown for paragraphs, lists, emphasis, and links." }));
    } else {
      const upload = node("label", "", { class: "field upload-field" });
      upload.append(node("span", "Upload image", { class: "field-label" }));
      const input = node("input", "", { type: "file", accept: "image/png,image/jpeg,image/webp,image/gif" });
      input.addEventListener("change", async () => {
        const file = input.files[0];
        if (!file) return;
        if (file.size > 15 * 1024 * 1024) { status("Choose an image smaller than 15 MB.", true); input.value = ""; return; }
        busy(true); status("Uploading image…");
        try {
          const result = await api("/api/upload", { method: "POST", body: file, headers: { "Content-Type": file.type || "application/octet-stream", "X-Filename": encodeURIComponent(file.name) } });
          block.src = result.src; dirty(); renderBlocks(item);
          status("Image uploaded. Add its description and caption, then save your changes.");
        } catch (error) { status(error.message, true); }
        finally { busy(false); }
      });
      upload.append(input); card.append(upload);
      card.append(field("Image path", block.src, value => block.src = value, { required: true, help: "Filled automatically when you upload. You can also use an existing local image path." }));
      if (/^\/(assets\/images|images)\/[A-Za-z0-9_./-]+$/.test(block.src)) card.append(node("img", "", { src: block.src, alt: block.alt || "Image preview", class: "image-preview" }));
      card.append(field("Image description", block.alt, value => block.alt = value, { required: true, maxLength: 2000, help: "Describe the important visual information for readers who cannot see the image." }));
      card.append(field("Caption (optional)", block.caption, value => block.caption = value, { textarea: true, maxLength: 2000 }));
      card.append(field("Image width", block.size, value => block.size = value, { select: [["full", "Full content width"], ["medium", "Medium · centred"]] }));
    }
    container.append(card);
  });
}

function render() {
  renderList();
  const item = current();
  if (!item) return;
  byId("item-kind").textContent = state.kind === "projects" ? "Project case study" : "Research direction";
  byId("item-heading").textContent = item.title;
  byId("preview-link").href = state.kind === "projects" ? `/preview/portfolio/${state.selected}/` : `/preview/research/${state.selected}/`;
  renderMetadata(item); renderBlocks(item);
  byId("editor-fields").disabled = state.busy;
}

async function save() {
  if (!byId("editor-form").reportValidity()) throw new Error("Complete the required fields before saving.");
  const result = await api("/api/content", { method: "PUT", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ projects: state.content.projects, research: state.content.research, revisions: state.content.revisions }) });
  state.content = result; state.dirty = false;
  byId("saved-state").textContent = "Saved"; byId("saved-state").classList.remove("dirty");
  render();
  status("Changes saved. Rebuild the preview to see them on the website.");
}

async function watchBuild() {
  busy(true);
  try {
    while (true) {
      const job = await api("/api/build");
      byId("build-details").hidden = false; byId("build-log").textContent = job.log;
      if (job.state !== "running") {
        if (job.state === "complete") {
          const link = byId("preview-link");
          link.href = link.href.split("?")[0] + (link.hash ? "" : `?built=${Date.now()}`);
          status("Preview rebuilt successfully. Open the site preview to review your changes.");
        } else if (job.state === "failed") {
          byId("build-details").open = true;
          status("The preview build failed. Your saved content is intact; see the build details below.", true);
        }
        break;
      }
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  } catch (error) { status(error.message, true); }
  finally { busy(false); }
}

byId("import-word").addEventListener("click", async () => {
  if (state.busy) return;
  if (state.dirty && !confirm("Importing replaces unsaved editor changes. Continue with your saved Word documents?")) return;
  busy(true); status("Importing new or changed Word documents from the content folders…");
  try {
    const result = await api("/api/import", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ revisions: state.content.revisions }) });
    state.content = result.content; state.dirty = false;
    if (!current()) state.selected = entries()[0][0];
    byId("saved-state").textContent = "Saved"; byId("saved-state").classList.remove("dirty");
    render(); status(result.message);
  } catch (error) { status(error.message, true); }
  finally { busy(false); }
});
byId("editor-form").addEventListener("submit", event => event.preventDefault());
byId("save").addEventListener("click", async () => {
  if (state.busy || !byId("editor-form").reportValidity()) return;
  busy(true);
  try { await save(); } catch (error) { status(error.message, true); }
  finally { busy(false); }
});
byId("build").addEventListener("click", async () => {
  if (state.busy || !byId("editor-form").reportValidity()) return;
  busy(true);
  try {
    if (state.dirty) await save();
    await api("/api/build", { method: "POST" });
    status("Building the website preview and checking its links…");
    await watchBuild();
  } catch (error) { status(error.message, true); busy(false); }
});
for (const kind of ["projects", "research"]) byId(`${kind}-tab`).addEventListener("click", () => { state.kind = kind; state.selected = entries()[0][0]; render(); });
byId("add-text").addEventListener("click", () => { current().blocks.push({ type: "text", heading: "", body: "" }); dirty(); renderBlocks(current()); });
byId("add-image").addEventListener("click", () => { current().blocks.push({ type: "image", src: "", alt: "", caption: "", size: "full" }); dirty(); renderBlocks(current()); });
byId("add-item").addEventListener("click", () => {
  const id = prompt(state.kind === "projects" ? "Choose a project URL name, for example urban-reconstruction:" : "Choose a research section name, for example urban-reconstruction:");
  if (id === null) return;
  if (!/^[a-z0-9][a-z0-9-]{0,79}$/.test(id)) { status("Use lowercase letters, numbers, and hyphens for the name.", true); return; }
  const item = { title: "New " + (state.kind === "projects" ? "project" : "research direction"), summary: "", blocks: [] };
  if (state.kind === "projects") {
    if (state.content.projects[id]) { status("A project with that URL name already exists.", true); return; }
    Object.assign(item, { context: "", role: "", order: Math.min(1000, Math.max(...Object.values(state.content.projects).map(project => project.order)) + 1), featured: false, research_anchor: "" });
    state.content.projects[id] = item;
  } else {
    if (state.content.research.modules.some(module => module.id === id)) { status("A research section with that name already exists.", true); return; }
    item.id = id; state.content.research.modules.push(item);
  }
  state.selected = id; dirty(); render();
});
byId("remove-item").addEventListener("click", () => {
  if (entries().length === 1) { status("Keep at least one item in each section.", true); return; }
  if (!confirm("Remove this item? The change takes effect when you save, and the previous content is backed up locally.")) return;
  if (state.kind === "projects") delete state.content.projects[state.selected];
  else {
    state.content.research.modules = state.content.research.modules.filter(module => module.id !== state.selected);
    for (const item of Object.values(state.content.projects)) if (item.research_anchor === state.selected) item.research_anchor = "";
  }
  state.selected = entries()[0][0]; dirty(); render();
});
window.addEventListener("beforeunload", event => { if (state.dirty) { event.preventDefault(); event.returnValue = ""; } });

(async () => {
  try {
    state.content = await api("/api/content"); state.token = state.content.token;
    state.selected = entries()[0][0]; render();
    status("Choose a project or research direction to edit. Changes are saved locally.");
    if ((await api("/api/build")).state === "running") { status("A preview build is running…"); await watchBuild(); }
  } catch (error) { status(error.message, true); busy(true); }
})();
