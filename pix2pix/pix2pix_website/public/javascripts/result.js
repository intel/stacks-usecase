import {LitElement, html, css} from './lit-element.min.js';

class Result extends LitElement {

    static get properties() {
      return {
        done: { type: Boolean },
        startImg: { type: String },
        renderedImg: { type: String },
        classes: { type: String },
        styles: { type: String },
        height: { type: String },
        callback: {type: Function }
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
          height: 95%;
          width: 100%;
          justify-content: space-evenly;
          box-sizing: border-box;
        }

        #performance {
          height: 4%;
          width: 100%;
          text-align: center;
          font-family: monospace;
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
      this.startImg = "";
      this.renderedImg = "";
      this.classes = "";
      this.styles = "";
      this.resultText = "Render times\n Unoptimized: 3934ms\n Optimized: 2482ms";
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
        <div id='performance'>${this.resultText}</div>
      </div>
      `;
    }
  }

  customElements.define('result-item', Result);