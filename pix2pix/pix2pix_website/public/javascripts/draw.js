'use strict';
import {LitElement, html, css} from './lit-element.min.js';
class DrawPage extends LitElement {

  static get properties() {
    return {
      daCVS: { type: Object },
      daCTX: { type: Object },
      preCVS: { type: Object },
      preCTX: { type: Object },
      smallCVS: { type: Object },
      smallCTX: { type: Object },
      mouseX: { type: Number },
      mouseY: { type: Number },
      lastMouseX: { type: Number },
      lastMouseY: { type: Number },
      mousedown: { type: Boolean },
      editImg: {type: Object },
      color: { type: String }
    };
  }

  static get styles() {
    return css`
    #container {
      width: 100%;
      height: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
      border-radius: 18px;
    }

    #drawingArea{
      height: 98%;
      z-index:3;
    }

    #drawingAreaOrig {
      width: 85%;
      height: 98%;
      z-index: 2;
    }

    #preImage {
      position: absolute;
      z-index:2;
    }

    #smallCanvas {
      position: absolute;
      z-index:1;
    }

    #selector {
      width: 12%;
      height: 98%;
      padding-right: 8px;
    }
`;
  }

  constructor() {
    super();
    this.mousedown = false;
    this.mouseX = this.mouseY = this.lastMouseX = this.lastMouseY = 0;
    this.editImg = undefined;
  }

  render() {
    return html`
      <div id='container'>
        <color-select id='selector' @colorselected=${this.setColor} @clearscreen=${this.clearScreen} ></color-select>
        <canvas id='drawingArea'></canvas>
        <canvas id='preImage'></canvas>
        <canvas id='smallCanvas'></canvas>
      </div>
`;
  }

  init() {
    // Reset the color selector
    this.shadowRoot.getElementById("selector").init();

    // Note this is required, otherwise canvas will be the default 300x150
    this.daCVS.width = this.preCVS.width = this.daCVS.clientHeight;
    this.daCVS.height = this.preCVS.height = this.daCVS.clientHeight;

    this.preCVS.style.left = this.smallCVS.style.left = this.daCVS.offsetLeft + "px";
    this.preCVS.style.top = this.smallCVS.style.top = this.daCVS.offsetTop + "px";

    this.smallCVS.width = 256;
    this.smallCVS.height = 256;

    this.clearScreen();
    // Display the image to edit if given one, otherwise create a blank canvas
    if (this.editImg !== undefined) {
      // pre-made images are smaller than the canvas, turn off smoothing to prevent too much blur
      this.preCTX.imageSmoothingEnabled = false;
      this.preCTX.drawImage(this.editImg, 0, 0, this.preCVS.width, this.preCVS.height);
      // Reset the edit file
      this.editImg = undefined;
    }
  }

  // A colorselected event was received from the color-select element, set the color using its data.
  setColor(color) {
    this.color = color.detail.data;
  }

  // Lit-element overloaded function. Gets called once the element is ready
  // In our case we are setting up our variables and click / touch events
  firstUpdated() {
    // This is the canvas the user draws on, it has the resizable rectangle
    this.daCVS = this.shadowRoot.getElementById("drawingArea");
    this.daCTX = this.daCVS.getContext("2d");
    // This is the actual drawing canvas, which has all the rectangles
    this.preCVS = this.shadowRoot.getElementById("preImage");
    this.preCTX = this.preCVS.getContext("2d");
    // This is the resize canvas, which is used to resize the image to the size the engine expects.
    this.smallCVS = this.shadowRoot.getElementById("smallCanvas");
    this.smallCTX = this.smallCVS.getContext("2d");

    this.addEventListener('mousedown', function(e) {
      this.lastMouseX = parseInt(e.clientX - this.daCVS.offsetLeft);
      this.lastMouseY = parseInt(e.clientY - this.daCVS.offsetTop);
      this.mousedown = true;
    });

    this.addEventListener('mouseup', function(e) {
      this.drawRect();
    });

    // Handle offscreen mouse releases
    window.addEventListener('mouseup', function(e) {
      if (this.mousedown) {
        this.drawRect();
      }
      this.mouseX = this.lastMouseX = undefined;
      this.mouseY = this.lastMouseY =undefined;
    }.bind(this));

    this.addEventListener('mousemove', function(e) {
      this.mouseX = parseInt(e.clientX - this.daCVS.offsetLeft);
      this.mouseY = parseInt(e.clientY - this.daCVS.offsetTop);
      // Draw the rectangle that shows what you have drawn so far, it won't be permenent
      // until you let go of the mouse.
      if(this.mousedown) {
        this.daCTX.clearRect(0,0,this.daCVS.clientWidth, this.daCVS.height);
        this.daCTX.beginPath();
        var width = this.mouseX - this.lastMouseX;
        var height = this.mouseY - this.lastMouseY;
        this.daCTX.rect(Math.floor(this.lastMouseX), Math.floor(this.lastMouseY) , Math.floor(width), Math.floor(height));
        this.daCTX.fillStyle = this.color;
        this.daCTX.fill();
      }
    });

    // Touch listeners
    this.addEventListener('touchstart', function(e) {
      this.lastMouseX = parseInt(e.touches[0].clientX - this.daCVS.offsetLeft);
      this.lastMouseY = parseInt(e.touches[0].clientY - this.daCVS.offsetTop);
      this.mousedown = true;
    });

    this.addEventListener('touchend', function(e) {
      this.drawRect();
      this.mouseX = this.lastMouseX = undefined;
      this.mouseY = this.lastMouseY =undefined;
    });

    this.addEventListener('touchmove', function(e) {
      this.mouseX = parseInt(e.touches[0].clientX - this.daCVS.offsetLeft);
      this.mouseY = parseInt(e.touches[0].clientY - this.daCVS.offsetTop);
      // Draw the rectangle that shows what you have drawn so far, it won't be permenent
      // until you let go of the mouse.
      if(this.mousedown) {
        this.daCTX.clearRect(0,0,this.daCVS.clientWidth, this.daCVS.height);
        this.daCTX.beginPath();
        var width = this.mouseX - this.lastMouseX;
        var height = this.mouseY - this.lastMouseY;
        this.daCTX.rect(Math.floor(this.lastMouseX), Math.floor(this.lastMouseY) , Math.floor(width), Math.floor(height));
        this.daCTX.fillStyle = this.color;
        this.daCTX.fill();
      }
    });
  }

  // Draw the rectangle permenently onto the canvas.
  drawRect() {
    // Make sure we have valid places to draw.
    if (this.lastMouseX === undefined || this.lastMouseY === undefined || this.mouseX === undefined || this.mouseY === undefined) {
      return;
    }
    this.mousedown = false;
    this.preCTX.beginPath();
    var width = this.mouseX - this.lastMouseX;
    var height = this.mouseY - this.lastMouseY;
    this.preCTX.rect(Math.floor(this.lastMouseX), Math.floor(this.lastMouseY) , Math.floor(width), Math.floor(height));
    this.preCTX.fillStyle = this.color;
    this.preCTX.fill();

    this.daCTX.clearRect(0,0,this.daCVS.clientWidth, this.daCVS.height);
  }

  clearScreen() {
    // Clear the top
    this.daCTX.beginPath();
    this.daCTX.clearRect(0,0,this.daCVS.clientWidth, this.daCVS.height);
    // Make the canvas into wall color again
    this.preCTX.beginPath();
    this.preCTX.rect(0, 0, this.preCVS.width, this.preCVS.height);
    this.preCTX.fillStyle = "#0d3dfb";
    this.preCTX.fill();
  }
}

customElements.define('draw-page', DrawPage);
