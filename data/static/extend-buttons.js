/* eslint-disable no-undef, semi */
Trix.config.blockAttributes.subHeadingh2 = { tagName: "h2" }
Trix.config.blockAttributes.subHeadingh3 = { tagName: "h3" }
Trix.config.blockAttributes.subHeadingh4 = { tagName: "h4" }
Trix.config.blockAttributes.subHeadingh5 = { tagName: "h5" }
Trix.config.blockAttributes.subHeadingh6 = { tagName: "h6" }
Trix.config.blockAttributes.p = { tagName: "p" }
/* eslint-enable no-undef */

const h2ButtonHTML =
  '<button type="button" class="trix-button" data-trix-attribute="subHeadingh2" title="Subheading H2">H2</button>'
const h3ButtonHTML =
  '<button type="button" class="trix-button" data-trix-attribute="subHeadingh3" title="Subheading H3">H3</button>'
const h4ButtonHTML =
  '<button type="button" class="trix-button" data-trix-attribute="subHeadingh4" title="Subheading H4">H4</button>'
const h5ButtonHTML =
  '<button type="button" class="trix-button" data-trix-attribute="subHeadingh5" title="Subheading H5">H5</button>'
const h6ButtonHTML =
  '<button type="button" class="trix-button" data-trix-attribute="subHeadingh6" title="Subheading H6">H6</button>'
const pButtonHTML =
  '<button type="button" class="trix-button" data-trix-attribute="p" title="p">P</button>'

document.addEventListener("trix-before-initialize", (event) => {
  const { toolbarElement } = event.target

  const trixTitleButton = toolbarElement.querySelector(
    "[data-trix-attribute=heading1]",
  )
  trixTitleButton.insertAdjacentHTML("afterend", pButtonHTML)
  trixTitleButton.remove()

  const p = toolbarElement.querySelector("[data-trix-attribute=p]")
  p.insertAdjacentHTML("afterend", h2ButtonHTML)

  const h2Button = toolbarElement.querySelector(
    "[data-trix-attribute=subHeadingh2]",
  )
  h2Button.insertAdjacentHTML("afterend", h3ButtonHTML)

  const h3Button = toolbarElement.querySelector(
    "[data-trix-attribute=subHeadingh3]",
  )
  h3Button.insertAdjacentHTML("afterend", h4ButtonHTML)

  const h4Button = toolbarElement.querySelector(
    "[data-trix-attribute=subHeadingh4]",
  )
  h4Button.insertAdjacentHTML("afterend", h5ButtonHTML)

  const h5Button = toolbarElement.querySelector(
    "[data-trix-attribute=subHeadingh5]",
  )
  h5Button.insertAdjacentHTML("afterend", h6ButtonHTML)
})
/* eslint-enable semi */
