import {LitElement, html, css} from './lit-element.min.js';

class ColorSelect extends LitElement {

    static get properties() {
      return {
        colors: { type: Array }
      };
    }

    static get styles() {
      return css`

      #container {
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
      }

      .colorItem {
        width: 86%;
        min-height: 30px;
        line-height: 30px;
        user-select: none;
        justify-content: center;
        margin: 5px;
        border-style: none;
        border-color: white;
        border-width: 3px;
        border-radius: 5px;
        font-family: Arial;
        font-size: 20px;
        text-align: center;
        font-weight: bold;
        color:#ffffff;
        text-shadow: 2px 2px 0 rgba(0, 0, 0, 0.2), 2px -2px 0 rgba(0, 0, 0, 0.2), -2px 2px 0 rgba(0, 0, 0, 0.2), -2px -2px 0 rgba(0, 0, 0, 0.2), 2px 0px 0 rgba(0, 0, 0, 0.2), 0px 2px 0 rgba(0, 0, 0, 0.2), -2px 0px 0 rgba(0, 0, 0, 0.2), 0px -2px 0 rgba(0, 0, 0, 0.2);
        cursor:pointer;
        vertical-align: middle;

      }

      .colorItem.selected {
        animation-name: change;
        animation-duration: 0.2s;
        font-size: 24px;
        border-radius: 15px;
        width: 100%;
      }

      @keyframes change {
        from {
          font-size: 20px;
          border-radius: 5px;
          width: 86%;
        }
        to {
          font-size: 24px;
          border-radius: 15px;
          width: 100%;
        }
      }

      .customButton {
        width: 80%;
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

      .customButton:hover {
        background:linear-gradient(to bottom, #e9e9e9 5%, #00e1ff 100%);
        box-shadow: 0px 1px 5px 5px #00ffff9c;
        background-color:#e9e9e9;
      }

      #renderBtn {
        background:linear-gradient(to bottom, #404040 5%, #4dff00 100%);
      }

      #renderBtn:hover {
        background:linear-gradient(to bottom, #e9e9e9 5%, #8cff8a 100%);
        box-shadow: 0px 1px 5px 5px #88ff599c;
        background-color:#e9e9e9;
      }
  `;
    }

    constructor() {
      super();
      this.colors = [ {text: "Background", rgb: "background-color: #0006d9"},
                      {text: "Wall", rgb: "background-color: #0d3dfb"},
                      {text: "Door", rgb: "background-color: #a50000"},
                      {text: "Window", rgb: "background-color: #0075ff"},
                      {text: "Window sill", rgb: "background-color: #68f898"},
                      {text: "Window head", rgb: "background-color: #1dffdd"},
                      {text: "Shutter", rgb: "background-color: #eeed28"},
                      {text: "Balcony", rgb: "background-color: #b8ff38"},
                      {text: "Trim", rgb: "background-color: #ff9204"},
                      {text: "Cornice", rgb: "background-color: #ff4401"},
                      {text: "Column", rgb: "background-color: #f60001"},
                      {text: "Entrance", rgb: "background-color: #00c9ff"}
      ];
    }

    render() {
      return html`
        <div id='container'>
          ${this.colors.map(i => html`<div class='colorItem' id=${i.text} style=${i.rgb} @click=${this.colorSelected}>${i.text}</div>`)}
          <button id='clear' class='customButton' @click=${this.clearScreen}>Clear</button>
          <button id="renderBtn" class=customButton @click="${this.renderClick}">Render</button>
        </div>
  `;
    }

    init() {
      var colors = this.shadowRoot.querySelectorAll(".selected");

      colors.forEach(function(el) {
        el.classList.remove("selected");
      });

      this.shadowRoot.getElementById("Window").click();
    }

    colorSelected(ev) {
      var colors = this.shadowRoot.querySelectorAll(".selected");
      // Unselect the current color
      colors.forEach(function(el) {
        el.classList.remove("selected");
      });
      // Find the color that got the click event
      var colorEl = ev.composedPath().find(function(i) { return i.classList.contains("colorItem");});
      colorEl.classList.add('selected');
      // Emit a color selected event to the draw element
      let event = new CustomEvent('colorselected', {
        detail: {
          message: 'Selected color',
          data: colorEl.style.backgroundColor
        }
      });
      this.dispatchEvent(event);
    }

    clearScreen() {
      let event = new CustomEvent('clearscreen', {
        detail: {
          message: 'Clear the screen'
        }
      });
      this.dispatchEvent(event);
    }

    renderClick() {
      var smallCVS = this.parentNode.children.smallCanvas;
      var smallCTX = smallCVS.getContext("2d");
      smallCTX.drawImage(this.parentNode.children.preImage, 0, 0, 256, 256);
      var preCVS = this.parentNode.children.preImage;
      var dataBuffer = smallCVS.toDataURL('image/jpg');
      var origBuffer = preCVS.toDataURL('image/jpg');
      let event = new CustomEvent('newdrawing', {
        detail: {
          message: 'Drawing rendering..',
          origBuff: origBuffer,
          imgBuff: dataBuffer
        },
        bubbles: true,
        composed: true
      });
      this.dispatchEvent(event);
    }
  }

  customElements.define('color-select', ColorSelect);
