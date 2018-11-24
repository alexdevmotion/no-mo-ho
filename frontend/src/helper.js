export class Helper {
  static applyStyleOnNode (node, styles) {
    let stylesArr = [];
    Object.keys(styles).forEach(style => {
      stylesArr.push(`${style}: ${styles[style]}`);
    });
    node.setAttribute('style', stylesArr.join(';'));
  }
}

export const magic = {
  TOP_OFFSET: 10,
  CONTAINER_WIDTH: 400,
};
