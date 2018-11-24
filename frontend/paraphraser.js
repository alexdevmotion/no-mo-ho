import { Helper, magic } from './helper';

function createHeader (options) {
  const span = document.createElement('span');
  span.style.flex = '1';
  span.innerText = 'It looks like this is offensive language.';

  const closeBtn = document.querySelector('div[aria-label="Dismiss"]').cloneNode(true);
  closeBtn.style.display = 'flex';
  closeBtn.style.cursor = 'pointer';
  closeBtn.addEventListener('click', options.onClose);

  const header = document.createElement('div');
  const headerStyles = {
    background: '#f5f6f7',
    padding: '10px',
    display: 'flex',
    'align-items': 'center',
    'font-size': '1.5em',
    'border-bottom': '1px solid black',
  };
  Helper.applyStyleOnNode(header, headerStyles);

  header.appendChild(span);
  header.appendChild(closeBtn);

  return header;
}

function createBody (options) {

  function createParagraph () {
    const span = document.createElement('span');
    span.innerText = 'You may end up being banned form the site. How about changing the text to one of the following:';
    return span;
  }

  function createHr () {
    return document.createElement('hr');
  }

  function createOptions () {
    const options = document.createElement('div');
    const optionsStyles = {
    };

    Helper.applyStyleOnNode(options, optionsStyles);
    options.setAttribute('class', 'noho-options');
    return options;
  }

  const body = document.createElement('div');
  const bodyStyles = {
    background: 'white',
    padding: '10px',
    'font-size': '1.1em',
  };

  Helper.applyStyleOnNode(body, bodyStyles);
  body.appendChild(createParagraph());
  body.appendChild(createHr());
  body.appendChild(createOptions());
  return body;
}

function createMainContainer (options) {
  const container = document.createElement("div");
  const styles = {
    background: 'white',
    overflow: 'hidden',
    border: '1px solid black',
    'border-radius': '3%',
    'font-size': '1em',
  };

  Helper.applyStyleOnNode(container, styles);
  container.appendChild(createHeader(options));
  container.appendChild(createBody(options));

  return container;
}

function createPointer (options) {
  const pointer = document.createElement("div");
  const styles = {
    width: 0,
    height: 0,
    'align-self': 'center',
    'border-left': '10px solid transparent',
    'border-right': '10px solid transparent',
    'border-bottom': '10px solid black',
    'border-top': 0,
  };

  Helper.applyStyleOnNode(pointer, styles);

  return pointer;
}

export function createParaphraser (options) {
  const node = document.createElement("div");
  const styles = {
    width: `${magic.CONTAINER_WIDTH}px`,
    position: 'absolute',
    left: options.coords.x + 'px',
    top: options.coords.y + 'px',
    display: 'flex',
    'flex-direction': 'column',
    'z-index': 10000
  };

  node.setAttribute('id', options.id);
  node.addEventListener('click', ev => ev.stopPropagation());
  Helper.applyStyleOnNode(node, styles);
  node.appendChild(createPointer(options));
  node.appendChild(createMainContainer(options));

  return node;

}

export function createOption (text, onSelect) {
  const option = document.createElement('div');
  const styles = {
    padding: '2px',
    'border-radius': '2%',
    'font-weight': 'bold',
  };

  Helper.applyStyleOnNode(option, styles);

  option.innerText = '> ' + text;
  option.addEventListener('click', onSelect.bind(null, text));

  return option;
}