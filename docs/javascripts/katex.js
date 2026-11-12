// 统一的矢量记号宏：\vv{E} = 粗斜体矢量，\ax 等 = 单位矢量 a_x ...
const EMMACROS = {
  "\\vv": "\\boldsymbol{#1}",
  "\\ax": "\\boldsymbol{a}_x", "\\ay": "\\boldsymbol{a}_y", "\\az": "\\boldsymbol{a}_z",
  "\\arho": "\\boldsymbol{a}_\\rho", "\\aphi": "\\boldsymbol{a}_\\phi",
  "\\ar": "\\boldsymbol{a}_r", "\\atheta": "\\boldsymbol{a}_\\theta", "\\an": "\\boldsymbol{a}_n",
  "\\dd": "\\mathrm{d}", "\\je": "\\mathrm{j}",
  "\\grad": "\\nabla", "\\divg": "\\nabla\\cdot", "\\curl": "\\nabla\\times",
  "\\Re": "\\operatorname{Re}", "\\Im": "\\operatorname{Im}"
};
document$.subscribe(() => {
  renderMathInElement(document.body, {
    delimiters: [
      { left: "$$",  right: "$$",  display: true },
      { left: "$",   right: "$",   display: false },
      { left: "\\(", right: "\\)", display: false },
      { left: "\\[", right: "\\]", display: true }
    ],
    macros: EMMACROS,
    throwOnError: false
  });
});
