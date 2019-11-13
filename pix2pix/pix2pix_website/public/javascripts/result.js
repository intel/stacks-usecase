'use strict';
import {LitElement, html, css} from './lit-element.min.js';

class Result extends LitElement {

    static get properties() {
      return {
        done: { type: Boolean },
        origImg: { type: String },
        startImg: { type: String },
        renderedImg: { type: String },
        classes: { type: String },
        styles: { type: String },
        height: { type: String },
        callback: {type: Function },
        reqID: { type: Number },
        addEdit: {type: Boolean }
      };
    }

    static get styles() {
      return css`
        #result {
          box-shadow: 0 4px 2px 0 rgba(0, 0, 0, 0.14), 0 1px 5px 0 rgba(0, 0, 0, 0.12), 0 3px 1px -2px rgba(0, 0, 0, 0.2);
          padding: 10px;
          border-radius: 8px;
          background-color: #fff;
          color: #757575;
          display: flex;
          flex-direction: column;
          align-items: center;
          height: 100%;
          box-sizing: border-box;
        }

        #images {
          display: flex;
          align-items: center;
          min-height: 85%;
          width: 100%;
          justify-content: space-evenly;
          box-sizing: border-box;
        }

        #editBtn {
          width: 12%;
          margin: 15px;
          text-align: center;
          box-shadow:inset 0px 1px 0px 0px #ffffff;
          background-color:#f9f9f9;
          border-radius:6px;
          cursor:pointer;
          color:#ffffff;
          font-family:Arial;
          font-size:20px;
          font-weight:bold;
          padding:11px 21px;
          text-shadow:1px 3px 3px #000000;
          background:linear-gradient(to bottom, #404040 5%, #4dff00 100%);
          display: none;
        }

        #editBtn:hover {
          background:linear-gradient(to bottom, #e9e9e9 5%, #8cff8a 100%);
          box-shadow: 0px 1px 5px 5px #88ff599c;
          background-color:#e9e9e9;
        }

        #origImg {
          display: none;
        }

        .editEnabled {
          display: block;
        }
        .imgDiv {
            display: flex;
          align-items: center;
          height: 100%;
          justify-content: space-evenly;
          width: 50%;
          object-fit: contain;
        }

        img {
          max-height: 100%;
          max-width: 100%;
          object-fit: contain;
        }

        p {
          font-family: monospace;
          font-size: 26px;
          font-weight: 500;
        }

        .red {
          -webkit-animation: mymove 1s infinite;
          max-height: 100%;
          max-width: 50%;
          object-fit: contain;

          color: rgba(229, 0, 0, 1);
        }

        @keyframes mymove {
          50%{color: rgba(0, 0, 0, 0.0);}
        }

        .opening {
          animation-name: openPage;
          animation-timing-function: ease-out;
          animation-duration: 0.5s;
        }

        @keyframes openPage {
          from {
            opacity: 0.2;

          }
          to {
            opacity: 1;

          }
        }
      `;
    }

    constructor() {
      super();
      this.done = false;
      this.origImg = "";
      this.startImg = "";
      this.renderedImg = "";
      this.classes = "";
      this.styles = "";
      this.resultText = "Render times\n Unoptimized: 3934ms\n Optimized: 2482ms";
      this.addEdit = false;
      this.reqID = -1; // Allows us to match up which starting image the incoming rendered image is for.
    }

    render() {
      return html`
      <div id="result" class="${this.classes}" style=${this.styles}>
        <div id='images'>
            <div class="imgDiv">
            <image id="startImg" src=${this.startImg} draggable="false"></image>
            </div>
            <div class="imgDiv">
            ${!this.done ?
                html`<p class="red">Working...</p>`:
                html`<image id="rendered" class="opening" src=${this.renderedImg} draggable="false"></image>`
            }
            </div>
        </div>
        <button id="editBtn" class=customButton @click="${this.editClick}">Edit</button>
      </div>
      <img id='origImg' src=${this.origImg} draggable="false">
      `;
    }
    firstUpdated() {
      if (this.addEdit === true) {
        this.enableEdit();
      }
    }

    enableEdit() {
      this.shadowRoot.getElementById("editBtn").style.display = "block";
    }

    disableEdit() {
      this.shadowRoot.getElementById("editBtn").style.display = "none";
    }

    editClick() {
      // Make an event containing the original image URL
      let event = new CustomEvent('editDrawing', {
        detail: {
          message: 'Open drawing to edit.',
          imgData: this.shadowRoot.getElementById("origImg")
        },
        bubbles: true,
        composed: true
      });
      this.dispatchEvent(event);
    }
  }

  customElements.define('result-item', Result);