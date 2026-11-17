/* Sicce Studio Home Assistant sidebar panel. */

const DOMAIN = "sicce_contrall";

class SicceStudioPanel extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._devices = [];
    this._selected = "";
    this._busy = false;
    this._loaded = false;
    this.shadowRoot.innerHTML = `
      <style>
        :host { display:block; min-height:100vh; color:#eaf5fa; background:radial-gradient(ellipse at 88% 0%,#123f5b 0,transparent 45%),#091725; font-family:var(--paper-font-body1_-_font-family,system-ui) }
        * { box-sizing:border-box } header { height:76px; display:flex; align-items:center; gap:13px; padding:12px 24px; border-bottom:1px solid #244258; background:#0c1d2e }
        ha-menu-button { display:block } header img { width:42px; height:42px } header strong { font-size:19px; letter-spacing:-.5px } header small,.muted { color:#8ba9bd }
        main { max-width:1160px; padding:38px 28px 64px; margin:auto }.eyebrow { color:#39d7c2; font-size:11px; font-weight:800; letter-spacing:2px } h1 { font-size:clamp(30px,5vw,48px); line-height:1; letter-spacing:-2px; margin:10px 0 12px } p { color:#9bb4c6; line-height:1.55 }
        .toolbar { display:flex; gap:12px; margin:28px 0; flex-wrap:wrap; align-items:end }.toolbar label { color:#9bb4c6; font-size:12px; flex:1; min-width:220px; max-width:460px }.toolbar select { display:block; margin-top:7px; width:100% }
        button,select,input { color:inherit; font:inherit; border:1px solid #36566d; background:#142c40; border-radius:13px; padding:11px 13px } button { cursor:pointer } button:hover:enabled { background:#1b3c53 } button:disabled { cursor:default; opacity:.45 } button:focus-visible,select:focus-visible,input:focus-visible { outline:3px solid #48ddca; outline-offset:3px }.primary { background:#2acbb7; color:#062127; border-color:#2acbb7; font-weight:750 }.danger { color:#ffc0bc; border-color:#825a63 }
        .hero { display:grid; grid-template-columns:1.07fr .93fr; gap:22px }.card { background:#10273a; border:1px solid #28475e; border-radius:22px; padding:24px; box-shadow:0 18px 45px #00000020 }.status { display:inline-block; border-radius:20px; background:#1a4755; color:#83e9db; font-size:11px; padding:6px 10px }.dial { --level:0; width:218px; height:218px; margin:22px auto; border-radius:50%; display:grid; place-items:center; background:conic-gradient(from 225deg,#2ad8c0 calc(var(--level) * 2.7deg),#2b5067 0deg,#2b5067 270deg,transparent 270deg) }.dial::before { content:""; position:absolute; width:188px; height:188px; border-radius:50%; background:#10273a }.dial > div { position:relative; text-align:center }.dial b { display:block; font-size:52px; letter-spacing:-2px }.dial small { color:#91aabd; font-size:11px; letter-spacing:1.5px; text-transform:uppercase }
        .range { display:grid; grid-template-columns:1fr 76px 20px; align-items:center; gap:10px }.range input[type=range] { padding:0; accent-color:#30d6c0 }.range input[type=number] { width:76px }.actions { display:grid; grid-template-columns:repeat(2,1fr); gap:11px; margin-top:20px }.actions button { min-height:48px }.metrics { display:grid; grid-template-columns:repeat(3,1fr); gap:14px; margin-top:22px }.metric { padding:18px; border-radius:17px; background:#112d41; border:1px solid #294b63 }.metric small { color:#92aabd }.metric strong { display:block; font-size:21px; margin-top:8px; overflow-wrap:anywhere }.notice { margin:20px 0; padding:14px 16px; border-radius:14px; background:#16364b; color:#bce1e7 }.notice.error { background:#482a32; color:#ffd4cf }.empty { max-width:670px; padding:45px 0 } #content[hidden],#empty[hidden],#notice[hidden] { display:none!important } footer { margin-top:28px; color:#7f9eaf; font-size:12px }
        @media(max-width:720px) { header { padding:10px 14px } main { padding:28px 16px }.hero { grid-template-columns:1fr }.metrics { grid-template-columns:1fr }.toolbar { margin:22px 0 }.dial { width:190px; height:190px }.dial::before { width:164px; height:164px }.dial b { font-size:44px } }
      </style>
      <header><ha-menu-button></ha-menu-button><img src="/sicce_contrall_panel/sicce-studio-logo.png" alt=""><div><strong>Sicce Studio</strong><br><small>ContrAll pump control</small></div></header>
      <main>
        <div class="eyebrow">SICCE · HOME ASSISTANT</div><h1>Alles im Fluss.</h1><p>Leistung, Pause und Status deiner ContrAll-Pumpe an einem Ort.</p>
        <div class="toolbar"><label>Pumpe<select id="device" aria-label="Pumpe auswählen"></select></label><button id="refresh">Aktualisieren</button></div>
        <div id="notice" class="notice" role="status" hidden></div>
        <section id="empty" class="empty" hidden><h2>Keine Sicce-Entität gefunden</h2><p>Richte zuerst unter Einstellungen → Geräte &amp; Dienste die Integration Sicce ContrAll ein. Danach diese Seite neu laden.</p></section>
        <section id="content" hidden>
          <div class="hero"><article class="card"><span class="status" id="status">Status wird geladen</span><div class="dial" id="dial"><div><b id="speed">—</b><small>Pump speed · %</small></div></div><label for="speed-slider">Gewünschte Leistung</label><div class="range"><input id="speed-slider" type="range" min="5" max="100" step="1" aria-label="Pumpenleistung"><input id="speed-input" type="number" min="5" max="100" step="1" aria-label="Pumpenleistung in Prozent"><span>%</span></div><div class="actions"><button id="apply" class="primary">Leistung übernehmen</button><button id="refresh-data">Daten neu laden</button></div></article>
          <article class="card"><h2>Betriebssteuerung</h2><p>Pause nutzt den von Sicce bestätigten Feed-/Pause-Modus. Sie ist keine elektrische Netztrennung.</p><div class="actions"><button id="pause" class="danger">Pause / Stopp</button><button id="resume" class="primary">Weiter</button></div><p class="muted">Für eine zeitgesteuerte Pause verwende den in der Dokumentation enthaltenen Home-Assistant-Timer.</p></article></div>
          <div class="metrics"><div class="metric"><small>Controller</small><strong id="controller">—</strong></div><div class="metric"><small>Temperatur</small><strong id="temperature">—</strong></div><div class="metric"><small>Firmware</small><strong id="firmware">—</strong></div></div>
        </section><footer>Sicce Studio · Die Werte stammen aus der Sicce-ContrAll-Integration.</footer>
      </main>`;
    this.$("refresh").onclick = () => this._load();
    this.$("refresh-data").onclick = () => this._call("button", "press", this._current()?.refresh);
    this.$("device").onchange = () => { this._selected = this.$("device").value; this._render(); };
    this.$("speed-slider").oninput = () => { this.$("speed-input").value = this.$("speed-slider").value; };
    this.$("speed-input").oninput = () => { this.$("speed-slider").value = this.$("speed-input").value; };
    this.$("apply").onclick = () => this._setSpeed();
    this.$("pause").onclick = () => this._call("switch", "turn_on", this._current()?.pause, "Pumpe wird pausiert …");
    this.$("resume").onclick = () => this._call("switch", "turn_off", this._current()?.pause, "Pumpe wird fortgesetzt …");
  }

  $(id) { return this.shadowRoot.getElementById(id); }
  set narrow(value) { this.shadowRoot.querySelector("ha-menu-button").narrow = value; }
  set hass(hass) {
    this._hass = hass;
    this.shadowRoot.querySelector("ha-menu-button").hass = hass;
    if (this.isConnected && !this._loaded) this._load();
    else this._render();
  }
  connectedCallback() { if (this._hass && !this._loaded) this._load(); }
  disconnectedCallback() { this._loaded = false; }
  _message(text = "", error = false) { const e = this.$("notice"); e.textContent = text; e.hidden = !text; e.classList.toggle("error", error); }
  _current() { return this._devices.find((device) => device.id === this._selected) || this._devices[0]; }
  _state(entity) { return entity ? this._hass?.states?.[entity] : undefined; }
  _entity(group, domain, names) {
    return group.entities.find((item) => item.entity_id.startsWith(`${domain}.`) && names.some((name) =>
      item.entity_id.includes(name) || String(item.original_name || "").toLowerCase().includes(name.replaceAll("_", " "))))?.entity_id;
  }
  async _load() {
    if (!this._hass || this._busy) return;
    this._busy = true; this.$("refresh").disabled = true; this._message("Sicce-Geräte werden geladen …");
    try {
      const entities = await this._hass.callWS({ type: "config/entity_registry/list" });
      const relevant = entities.filter((entry) => entry.platform === DOMAIN && !entry.disabled_by);
      const groups = new Map();
      for (const entity of relevant) {
        const key = entity.device_id || "unassigned";
        if (!groups.has(key)) groups.set(key, { id:key, entities:[], name:null });
        groups.get(key).entities.push(entity);
      }
      this._devices = [...groups.values()].map((group, index) => {
        group.name = this._state(group.entities[0]?.entity_id)?.attributes?.device_name || `Sicce controller ${index + 1}`;
        group.speed = this._entity(group, "number", ["pump_speed", "speed", "power"]);
        group.pause = this._entity(group, "switch", ["pause"]);
        group.refresh = this._entity(group, "button", ["refresh"]);
        group.status = this._entity(group, "sensor", ["status"]);
        group.temperature = this._entity(group, "sensor", ["water_temperature", "temperature"]);
        group.firmware = this._entity(group, "sensor", ["firmware"]);
        return group;
      });
      const select = this.$("device"); select.replaceChildren(...this._devices.map((device) => {
        const option = document.createElement("option"); option.value = device.id; option.textContent = device.name; return option;
      }));
      this._selected = this._devices.some((device) => device.id === this._selected) ? this._selected : this._devices[0]?.id || "";
      select.value = this._selected; this._loaded = true; this._message(""); this._render();
    } catch (error) { this._message(`Geräte konnten nicht geladen werden: ${error.message || error}`, true); }
    finally { this._busy = false; this.$("refresh").disabled = false; }
  }
  _render() {
    const group = this._current(); const empty = !group;
    this.$("empty").hidden = !empty; this.$("content").hidden = empty; if (empty) return;
    const speed = Number(this._state(group.speed)?.state); const validSpeed = Number.isFinite(speed) && speed >= 0 && speed <= 100;
    this.$("speed").textContent = validSpeed ? String(speed) : "—"; this.$("dial").style.setProperty("--level", validSpeed ? speed : 0);
    this.$("speed-slider").value = validSpeed ? String(speed) : "5"; this.$("speed-input").value = validSpeed ? String(speed) : "";
    this.$("apply").disabled = !group.speed || this._busy; this.$("pause").disabled = !group.pause || this._busy; this.$("resume").disabled = !group.pause || this._busy; this.$("refresh-data").disabled = !group.refresh || this._busy;
    const pauseState = this._state(group.pause)?.state; this.$("status").textContent = pauseState === "on" ? "PAUSIERT" : "ONLINE";
    this.$("controller").textContent = this._state(group.status)?.state || "—"; this.$("temperature").textContent = this._display(group.temperature); this.$("firmware").textContent = this._state(group.firmware)?.state || "—";
  }
  _display(entity) { const state = this._state(entity); return state ? `${state.state}${state.attributes?.unit_of_measurement ? ` ${state.attributes.unit_of_measurement}` : ""}` : "—"; }
  async _call(domain, service, entity, message = "") {
    if (!entity || this._busy) return; this._busy = true; this._render(); this._message(message);
    try { await this._hass.callService(domain, service, { entity_id: entity }); this._message("Befehl ausgeführt. Der Controller wird aktualisiert."); }
    catch (error) { this._message(`Befehl fehlgeschlagen: ${error.message || error}`, true); }
    finally { this._busy = false; this._render(); }
  }
  async _setSpeed() {
    const group = this._current(); const value = Number(this.$("speed-input").value);
    if (!group?.speed || !Number.isInteger(value) || value < 5 || value > 100) { this._message("Bitte eine ganze Zahl zwischen 5 und 100 eingeben.", true); return; }
    this._busy = true; this._render(); this._message("Leistung wird gesetzt und bestätigt …");
    try { await this._hass.callService("number", "set_value", { entity_id: group.speed, value }); this._message("Leistungsbefehl ausgeführt."); }
    catch (error) { this._message(`Leistung konnte nicht gesetzt werden: ${error.message || error}`, true); }
    finally { this._busy = false; this._render(); }
  }
}

customElements.define("sicce-studio-panel", SicceStudioPanel);
