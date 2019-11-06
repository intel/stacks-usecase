import {LitElement, html, css} from './lit-element.min.js';
import './draw.js';
import './result.js';
import './history.js';
import './grid.js';
import './colorselect.js';

class PixDemoApp extends LitElement {

  static get properties() {
    return {
      resultArr: { type: Array },
      filesJSON: { type: String },
      reqID: { type: Number }
    };
  }

  constructor() {
    super();
    this.reqID = 0; // Allows us to match up which starting image the incoming rendered image is for.
  }

  static get styles() {
    return css`
    * {
      user-select: none;
    }

    #title {
      box-shadow: 0px 0px 20px 10px rgba(0, 150, 200, 0.1), -2px 0px 25px 15px rgba(0, 200, 100, 0.2), 2px 0px 10px 0px rgba(0, 100, 200, 0.9);
      font-family: sans-serif;
      font-size: 30px;
      font-weight: 500;
      text-shadow: 0 -1px 0 #fff, 0 1px 0 #2e2e2e, 0 2px 0 #2c2c2c, 0 3px 0 #2a2a2a, 0 4px 0 #282828, 0 5px 0 #262626, 0 6px 0 #242424, 0 7px 0 #222, 0 8px 0 #202020, 0 9px 0 #1e1e1e, 2px 2px 2px rgba(206,89,55,0);
      color: white;
      padding: 16px;
      margin: 24px;
      border-radius: 5px;
      background-color: rgba(45, 45, 45, .9);
      text-align: center;
      height: 100px;
      width: 60%;
    }

    #two {
      color: black;
      text-shadow: 2px 2px 0 white, 2px -2px 0 white, -2px 2px 0 white, -2px -2px 0 white, 2px 0px 0 white, 0px 2px 0 white, -2px 0px 0 white, 0px -2px 0 white;
    }

    #maincontent {
      height: 100vh;
      width: 100vw;
      background:linear-gradient(to bottom, #2d2d2d 5%,#ffffff 100%);
      display:flex;
      align-items: flex-start;
    }

    #sidebar {
      width: 15%;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
    }

    .page {
      display: none;
      margin: auto;
      height: 97%;
      width: 83%;
    }

    .customButton {
      width: 60%;
      margin: 15px;
      text-align: center;
      box-shadow:inset 0px 1px 0px 0px #ffffff;
      background:linear-gradient(to bottom, #404040 5%, #24a8a8 100%);
      background-color:#f9f9f9;
      border-radius:6px;
      cursor:pointer;
      color:#ffffff;
      font-family:Arial;
      font-size:20px;
      font-weight:bold;
      padding:11px 21px;
      text-shadow:1px 3px 3px #000000;
    }

    .customButton.enabled:hover {
      background:linear-gradient(to bottom, #e9e9e9 5%, #00e1ff 100%);
      box-shadow: 0px 1px 10px 10px #00ffff9c;
      background-color:#e9e9e9;
    }

    .open {
      animation-name: openPage;
      animation-timing-function: ease;
      animation-duration: 0.3s;
      height: 97%;
      width: 83%;
    }

    @keyframes openPage {
      from {
        opacity: 0.2;
      }
      to {
        opacity: 1;
      }
    }

    .customButton.enabled:active {
      top:1px;
    }

    #openfile {
      display: none;
    }

    p {
      color: #ffffff;
      font-family:Arial;
      font-size:18px;
      text-align: center;
    }
    `;
  }

  render() {
    return html`

    <div id="maincontent">
      <div id="sidebar">
        <h2 id="title"><b>P I X</br><span id="two">[ 2 ]</span></br>P I X</b></h2>
        <button id="drawBtn" class="customButton enabled" @click="${this.toggleDraw}">Draw your own</button>
        <button id="imageSelect" class="customButton enabled"  @click="${this.toggleImgSelect}">Image Select</button>
        <button id="histBtn" class="customButton enabled" @click="${this.toggleHistory} ">History</button>
      </div>
      <result-item id="selectedResult" class='page'}></result-item>
      <result-bar id="historyBar" class='page' @click=${this.maincb}></result-bar>
      <item-grid id="imgGrid" class='page' @click=${this.imgSelected} @renderimage=${this.renderImage}></item-grid>
      <draw-page id="drawPage" class='page' @renderimage=${this.renderImage} @newdrawing=${this.newDrawing}></draw-page>
    </div>
    `;
  }

  openView (openStr) {
    var openEl = this.shadowRoot.getElementById(openStr);
    var pages = this.shadowRoot.querySelectorAll('.page');

    pages.forEach(el => {
      el.style.display = 'none';
      el.classList.remove('open');
    });

    openEl.style.display = 'block';
    openEl.requestUpdate();
    openEl.classList.add('open');
  }

  maincb(ev) {
    var selRes = this.shadowRoot.getElementById('selectedResult');
    var ri = ev.composedPath().find(function(i) { return i.tagName == "RESULT-ITEM";});
    selRes.startImg = ri.startImg;
    selRes.done = true;
    selRes.renderedImg = ri.renderedImg;
    this.openView('selectedResult');
  }

  imgSelected(ev) {
    var selRes = this.shadowRoot.getElementById('selectedResult');
    var ri = ev.composedPath().find(function(i) { return i.tagName == "IMG";});
    this.openView('selectedResult');
    selRes.startImg = "../images/" + ri.getAttribute('data-filename');
    selRes.done = false;
    selRes.renderedImg = "";
    selRes.reqID = this.reqID;
    var formData = new FormData();
    formData.append("type", "FILESRC");
    formData.append("imgSrc", ri.getAttribute('data-filename'));
    formData.append("reqID", this.reqID++);
    fetch('/render', {
      method: 'POST',
      body: formData
    }).then (function(res){
      console.log(res);
      this.renderImage(res);
    }.bind(this));
  }


  toggleHistory() {
    var historyBar = this.shadowRoot.getElementById('historyBar');
    if (!historyBar.classList.contains('open')) {
      this.openView('historyBar');
    } else {
      this.openView('selectedResult');
    }
  }

  toggleImgSelect() {
    console.log("Clicking the open file");
    var imgSel = this.shadowRoot.getElementById('imgGrid');
    if (!imgSel.classList.contains('open')) {
      this.openView('imgGrid');
    } else {
      this.openView('selectedResult');
    }
  }

  toggleDraw() {
    var drawPage = this.shadowRoot.getElementById('drawPage');
    if (!drawPage.classList.contains('open')) {
      this.openView('drawPage');
      drawPage.init();
    } else {
      this.openView('selectedResult');
    }
  }

  renderImage(ev) {
    var filename = ev.json().then(function(replyJson){
      console.log(replyJson);
      var nocache = new Date().getTime();
      nocache = '?' + nocache;
      var selRes = this.shadowRoot.getElementById('selectedResult');
      // If the currently visible result is the one we got a result for, update it
      if (selRes.reqID === Number(replyJson.reqID)) {
        selRes.renderedImg = replyJson.renderedPath + '?' + nocache;
        selRes.done = true;
      }
      // Add result to the history
      this.shadowRoot.getElementById('historyBar').setItem(replyJson.startPath + nocache, replyJson.renderedPath + nocache);
    }.bind(this));

  }

  newDrawing(ev) {
    var imgBuff = ev.detail.imgBuff;
    var selRes = this.shadowRoot.getElementById('selectedResult');
    selRes.startImg = imgBuff;
    selRes.done = false;
    selRes.reqID = this.reqID;
    this.openView('selectedResult');

    var formData = new FormData();
    formData.append("type", "BUFFER");
    formData.append("imgData", ev.detail.imgBuff);
    formData.append("reqID", this.reqID++);
    // Send the data buffer to the server to be rendered
    fetch('/render', {
      method: 'POST',
      body: formData
    }).then (function(res){
      // Handle the reply
      console.log(res);
      this.renderImage(res);
    }.bind(this));
  }
}

customElements.define('pix-demo-app', PixDemoApp);
