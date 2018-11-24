import { createOption, createParaphraser } from './paraphraser';
import { magic } from './helper';
import { getReplaceText } from './service';
import { applyGlobalCSS, removeGlobalCSS } from './global-style';

let finalText;

(function(send) {
  const token = '%22text%22%3A';
  XMLHttpRequest.prototype.send = function(data) {
    if (data && data.contains(token)) {
      console.log(data);
      data = data.replace(/%22text%22%3A%22([a-zA-Z0-9]+)%22/, `%22text%22%3A%22${finalText}%22`);
    }
    send.call(this, data);
  };

})(XMLHttpRequest.prototype.send);

class Paraphraser {
  constructor (options) {
    this._init(options);
  }

  _init (options) {
    this.options = options || this._getDefaultParams();
    this.listeners = [];
    this.isOpen = false;
    this.userAgreed = false;
    this.isApplied = false;
  }

  _getDefaultParams () {
    return {
      textSelector: '[data-testid="status-attachment-mentions-input"]',
      postBtnSelector: 'button[data-testid="react-composer-post-button"]',
    }
  }

  _onClose (ev) {
    const body = document.getElementsByTagName('body')[0];
    this.isOpen = false;
    const node = document.getElementById('noho-paraphraser');
    node && body.removeChild(node);
  }

  _onContinue () {
    finalText = this.targetArea.innerHTML;
    this.postBtn.click();
    this.remove();
  }

  _insertTextReplaceOptionsContainer (coords = { x: 0, y: 0 }) {
    if (this.isOpen) return;
    const body = document.getElementsByTagName('body')[0];

    const options = {
      id: 'noho-paraphraser',
      coords,
      onClose: this._onClose.bind(this)
    };

    const paraphraser = createParaphraser(options);
    body.appendChild(paraphraser);
    paraphraser.scrollIntoView({ behavior: 'smooth' });
    this.isOpen = true;
  }

  _insetTextOptions (options) {
    if (!this.isOpen) return;

    const container = document.querySelector('#noho-paraphraser .noho-options');

    options.forEach(option => {
      const optionNode = createOption(option, selection => {
        this._onClose();
        this._removeHighlightOffensiveArea();
        this.targetArea.innerHTML = selection;
      });
      container.appendChild(optionNode);
    });

    const okWithIt = createOption('I don\'t care. Let me post.', () => {
      this.userAgreed = true;
      this._onClose();
      this._removeHighlightOffensiveArea();
      this._onContinue();
    });

    container.appendChild(okWithIt);
  }

  _highlightOffensiveArea () {
    document.querySelector(this.options.textSelector).style.border = '1px solid red';
  }

  _removeHighlightOffensiveArea () {
    document.querySelector(this.options.textSelector).style.border = 'none';
  }

  _applyAreaListener () {
    let l;
    l = document.addEventListener('click', this._onClose.bind(this));
    this.listeners.push({ type: 'keydown', listener: l });

    // l = document.addEventListener('keydown', ev => {
    //   const keyName = ev.key;
    //   console.log('keydown event key: ' + keyName);
    // });
    this.listeners.push({ type: 'keydown', listener: l });
    console.log('Applied area event');
  }

  _applyPostBtnListener () {
    console.log('Applied post btn event');
    const l = this.postBtn.addEventListener('click', async ev => {
      if (this.userAgreed) return;

      ev.stopPropagation();

      const result = await getReplaceText(document.querySelector(this.options.textSelector).innerHTML);
      if (!result.length) {
        this._onContinue();
        return;
      }

      const popupLoc = { x: +ev.pageX - (magic.CONTAINER_WIDTH / 2), y: +ev.pageY + magic.TOP_OFFSET };
      console.log(`Tried to post. Clicked on coords (${popupLoc.x}, ${popupLoc.y})`);

      this._highlightOffensiveArea();
      this._insertTextReplaceOptionsContainer(popupLoc);
      this._insetTextOptions(result);
    });
    this.listeners.push({ type: 'keydown', listener: l });
  }

  apply () {
    console.group('Applying paraphraser');
    this.isApplied = true;

    this.targetArea = document.querySelector(this.options.textSelector);
    this.targetArea.setAttribute('tab-index', '0');
    console.log('Caught text element:', this.targetArea);

    this.postBtn = document.querySelector(this.options.postBtnSelector);
    console.log('Caught post button:', this.postBtn);

    applyGlobalCSS();
    this._applyAreaListener();
    this._applyPostBtnListener();
    console.groupEnd();
  }

  remove () {
    console.log('Removing');
    this.isApplied = false;
    this.listeners.forEach(l => {
      document.removeEventListener(l.type, l.listener);
    });
    removeGlobalCSS();
    this._init();
  }
}

const para = new Paraphraser();

const checkExist = setInterval(() => {
  if (para.isApplied) {
    // Hack to check if the found button is actually the real one.
    const postBtn = document.querySelector(para.options.postBtnSelector);
    if (postBtn !== para.postBtn) { para.remove() }
    return;
  }

  const text = document.querySelector(para.options.textSelector);
  const postBtn = document.querySelector(para.options.postBtnSelector);

  if (text && postBtn) {
    para.apply();
  }
}, 1000);
