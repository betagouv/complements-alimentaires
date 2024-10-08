// Suite à https://github.com/Renovamen/oh-vue-icons/issues/24 et en attendant un fix,
// on import les icônes manuellement de frontend/node_modules/oh-vue-icons/icons/ri/index.js
// pour réduire la taille du bundle

// Helper
const remixIcon = (name, value) => {
  return {
    name: name,
    minX: 0,
    minY: 0,
    width: 24,
    height: 24,
    raw: `<path fill="none" d="M0 0h24v24H0z"/><path d="${value}"/>`,
  }
}

// Icons

export const RiLoginCircleLine = remixIcon(
  "ri-login-circle-line",
  "M10 11V8l5 4-5 4v-3H1v-2h9zm-7.542 4h2.124A8.003 8.003 0 0020 12 8 8 0 004.582 9H2.458C3.732 4.943 7.522 2 12 2c5.523 0 10 4.477 10 10s-4.477 10-10 10c-4.478 0-8.268-2.943-9.542-7z"
)
export const RiLogoutCircleLine = remixIcon(
  "ri-logout-circle-line",
  "M5 11h8v2H5v3l-5-4 5-4v3zm-1 7h2.708a8 8 0 100-12H4a9.985 9.985 0 018-4c5.523 0 10 4.477 10 10s-4.477 10-10 10a9.985 9.985 0 01-8-4z"
)
export const RiAccountCircleLine = remixIcon(
  "ri-account-circle-line",
  "M12 22C6.477 22 2 17.523 2 12S6.477 2 12 2s10 4.477 10 10-4.477 10-10 10zm-4.987-3.744A7.966 7.966 0 0012 20a7.97 7.97 0 005.167-1.892A6.979 6.979 0 0012.16 16a6.981 6.981 0 00-5.147 2.256zM5.616 16.82A8.975 8.975 0 0112.16 14a8.972 8.972 0 016.362 2.634 8 8 0 10-12.906.187zM12 13a4 4 0 110-8 4 4 0 010 8zm0-2a2 2 0 100-4 2 2 0 000 4z"
)
export const RiLogoutBoxRLine = remixIcon(
  "ri-logout-box-r-line",
  "M5 22a1 1 0 01-1-1V3a1 1 0 011-1h14a1 1 0 011 1v3h-2V4H6v16h12v-2h2v3a1 1 0 01-1 1H5zm13-6v-3h-7v-2h7V8l5 4-5 4z"
)
export const RiVideoChatLine = remixIcon(
  "ri-video-chat-line",
  "M14 10.25L17 8v6l-3-2.25V14H7V8h7v2.25zM5.763 17H20V5H4v13.385L5.763 17zm.692 2L2 22.5V4a1 1 0 011-1h18a1 1 0 011 1v14a1 1 0 01-1 1H6.455z"
)
// Ingredients icons
export const RiPlantLine = remixIcon(
  "ri-plant-line",
  "M6 2a7 7 0 016.197 3.741A6.49 6.49 0 0117.5 3H21v2.5a6.5 6.5 0 01-6.5 6.5H13v1h5v7a2 2 0 01-2 2H8a2 2 0 01-2-2v-7h5v-2H9a7 7 0 01-7-7V2h4zm10 13H8v5h8v-5zm3-10h-1.5A4.5 4.5 0 0013 9.5v.5h1.5A4.5 4.5 0 0019 5.5V5zM6 4H4a5 5 0 005 5h2a5 5 0 00-5-5z"
)
export const RiMicroscopeLine = remixIcon(
  "ri-microscope-line",
  "M13.196 2.268l3.25 5.63a1 1 0 01-.366 1.365l-1.3.75 1.001 1.732-1.732 1-1-1.733-1.299.751a1 1 0 01-1.366-.366L8.546 8.215a5.002 5.002 0 00-3.222 6.561A4.976 4.976 0 018 14c1.684 0 3.174.833 4.08 2.109l7.688-4.439 1 1.732-7.878 4.549A5.038 5.038 0 0112.9 20H21v2l-17 .001A4.979 4.979 0 013 19c0-1.007.298-1.945.81-2.73a7.001 7.001 0 013.717-9.82l-.393-.682a2 2 0 01.732-2.732l2.598-1.5a2 2 0 012.732.732zM8 16a3 3 0 00-2.83 4h5.66A3 3 0 008 16zm3.464-12.732l-2.598 1.5 2.75 4.763 2.598-1.5-2.75-4.763z"
)
export const RiFlaskLine = remixIcon(
  "ri-flask-line",
  "M16 2v2h-1v3.243c0 1.158.251 2.301.736 3.352l4.282 9.276A1.5 1.5 0 0118.656 22H5.344a1.5 1.5 0 01-1.362-2.129l4.282-9.276A7.994 7.994 0 009 7.243V4H8V2h8zm-2.612 8.001h-2.776c-.104.363-.23.721-.374 1.071l-.158.361L6.125 20h11.749l-3.954-8.567a9.978 9.978 0 01-.532-1.432zM11 7.243c0 .253-.01.506-.029.758h2.058a8.777 8.777 0 01-.021-.364L13 7.243V4h-2v3.243z"
)
export const RiContrastDrop = remixIcon(
  "ri-contrast-drop-line",
  "M12 3.09735L7.05025 8.04709C4.31658 10.7808 4.31658 15.2129 7.05025 17.9466C9.78392 20.6803 14.2161 20.6803 16.9497 17.9466C19.6834 15.2129 19.6834 10.7808 16.9497 8.0471L12 3.09735ZM12 0.268921L18.364 6.63288C21.8787 10.1476 21.8787 15.8461 18.364 19.3608C14.8492 22.8755 9.15076 22.8755 5.63604 19.3608C2.12132 15.8461 2.12132 10.1476 5.63604 6.63288L12 0.268921ZM12 17.9968V7.99684C14.7614 7.99684 17 10.2354 17 12.9968C17 15.7583 14.7614 17.9968 12 17.9968Z"
)
export const RiBubbleChart = remixIcon(
  "ri-bubble-chart-line",
  "M16 16C17.6569 16 19 17.3431 19 19C19 20.6569 17.6569 22 16 22C14.3431 22 13 20.6569 13 19C13 17.3431 14.3431 16 16 16ZM6 12C8.20914 12 10 13.7909 10 16C10 18.2091 8.20914 20 6 20C3.79086 20 2 18.2091 2 16C2 13.7909 3.79086 12 6 12ZM16 18C15.4477 18 15 18.4477 15 19C15 19.5523 15.4477 20 16 20C16.5523 20 17 19.5523 17 19C17 18.4477 16.5523 18 16 18ZM6 14C4.89543 14 4 14.8954 4 16C4 17.1046 4.89543 18 6 18C7.10457 18 8 17.1046 8 16C8 14.8954 7.10457 14 6 14ZM14.5 2C17.5376 2 20 4.46243 20 7.5C20 10.5376 17.5376 13 14.5 13C11.4624 13 9 10.5376 9 7.5C9 4.46243 11.4624 2 14.5 2ZM14.5 4C12.567 4 11 5.567 11 7.5C11 9.433 12.567 11 14.5 11C16.433 11 18 9.433 18 7.5C18 5.567 16.433 4 14.5 4Z"
)
export const RiFilter2 = remixIcon(
  "ri-filter-2-line",
  "M14 14V20L10 22V14L4 5V3H20V5L14 14ZM6.4037 5L12 13.3944L17.5963 5H6.4037Z"
)

// Substance icon
export const RiTestTubeLine = remixIcon(
  "ri-test-tube-line",
  "M17 2v2h-1v14c0 2.21-1.79 4-4 4s-4-1.79-4-4V4H7V2h10zm-3 8h-4v8a2 2 0 104 0v-8zm-1 5a1 1 0 110 2 1 1 0 010-2zm-2-3a1 1 0 110 2 1 1 0 010-2zm3-8h-4v4h4V4z"
)
export const RiArrowRightLine = remixIcon(
  "ri-arrow-right-line",
  "M16.172 11l-5.364-5.364 1.414-1.414L20 12l-7.778 7.778-1.414-1.414L16.172 13H4v-2z"
)
export const RiPriceTag2Fill = remixIcon(
  "ri-price-tag-2-fill",
  "M3 7l8.445-5.63a1 1 0 011.11 0L21 7v14a1 1 0 01-1 1H4a1 1 0 01-1-1V7zm9 4a2 2 0 100-4 2 2 0 000 4zm-4 5v2h8v-2H8zm0-3v2h8v-2H8z"
)
export const RiCapsuleFill = remixIcon(
  "ri-capsule-fill",
  "M19.778 4.222a6 6 0 010 8.485l-2.122 2.12-4.949 4.951a6 6 0 01-8.485-8.485l7.07-7.071a6.001 6.001 0 018.486 0zm-4.95 10.606L9.172 9.172l-3.536 3.535a4 4 0 005.657 5.657l3.535-3.536z"
)
export const RiFileUserFill = remixIcon(
  "ri-file-user-fill",
  "M16 2l5 5v14.008a.993.993 0 01-.993.992H3.993A1 1 0 013 21.008V2.992C3 2.444 3.445 2 3.993 2H16zm-4 9.5a2.5 2.5 0 100-5 2.5 2.5 0 000 5zM7.527 17h8.946a4.5 4.5 0 00-8.946 0z"
)
export const RiFocus2Fill = remixIcon(
  "ri-focus-2-fill",
  "M12 2c5.52 0 10 4.48 10 10s-4.48 10-10 10S2 17.52 2 12 6.48 2 12 2zm0 18c4.427 0 8-3.573 8-8s-3.573-8-8-8a7.99 7.99 0 00-8 8c0 4.427 3.573 8 8 8zm0-2c-3.32 0-6-2.68-6-6s2.68-6 6-6 6 2.68 6 6-2.68 6-6 6zm0-8c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"
)
export const RiHome4Line = remixIcon(
  "ri-home-4-line",
  "M19 21H5a1 1 0 01-1-1v-9H1l10.327-9.388a1 1 0 011.346 0L23 11h-3v9a1 1 0 01-1 1zm-6-2h5V9.157l-6-5.454-6 5.454V19h5v-6h2v6z"
)

export const RiArrowLeftLine = remixIcon(
  "ri-arrow-left-line",
  "M7.828 11H20v2H7.828l5.364 5.364-1.414 1.414L4 12l7.778-7.778 1.414 1.414z"
)

export const RiInformationLine = remixIcon(
  "ri-information-line",
  "M12 22C6.477 22 2 17.523 2 12S6.477 2 12 2s10 4.477 10 10-4.477 10-10 10zm0-2a8 8 0 100-16 8 8 0 000 16zM11 7h2v2h-2V7zm0 4h2v6h-2v-6z"
)

export const RiAttachment2 = remixIcon(
  "ri-attachment-2",
  "M14.828 7.757l-5.656 5.657a1 1 0 101.414 1.414l5.657-5.656A3 3 0 1012 4.929l-5.657 5.657a5 5 0 107.071 7.07L19.071 12l1.414 1.414-5.657 5.657a7 7 0 11-9.9-9.9l5.658-5.656a5 5 0 017.07 7.07L12 16.244A3 3 0 117.757 12l5.657-5.657 1.414 1.414z"
)

export const RiFileTextLine = remixIcon(
  "ri-file-text-line",
  "M21 8v12.993A1 1 0 0120.007 22H3.993A.993.993 0 013 21.008V2.992C3 2.455 3.449 2 4.002 2h10.995L21 8zm-2 1h-5V4H5v16h14V9zM8 7h3v2H8V7zm0 4h8v2H8v-2zm0 4h8v2H8v-2z"
)

export const RiDropLine = remixIcon(
  "ri-drop-line",
  "M12 3.1L7.05 8.05a7 7 0 109.9 0L12 3.1zm0-2.828l6.364 6.364a9 9 0 11-12.728 0L12 .272z"
)

export const RiEyeLine = remixIcon(
  "ri-eye-line",
  "M12 3c5.392 0 9.878 3.88 10.819 9-.94 5.12-5.427 9-10.819 9-5.392 0-9.878-3.88-10.819-9C2.121 6.88 6.608 3 12 3zm0 16a9.005 9.005 0 008.777-7 9.005 9.005 0 00-17.554 0A9.005 9.005 0 0012 19zm0-2.5a4.5 4.5 0 110-9 4.5 4.5 0 010 9zm0-2a2.5 2.5 0 100-5 2.5 2.5 0 000 5z"
)

export const RiEyeOffLine = remixIcon(
  "ri-eye-off-line",
  "M17.882 19.297A10.949 10.949 0 0112 21c-5.392 0-9.878-3.88-10.819-9a10.982 10.982 0 013.34-6.066L1.392 2.808l1.415-1.415 19.799 19.8-1.415 1.414-3.31-3.31zM5.935 7.35A8.965 8.965 0 003.223 12a9.005 9.005 0 0013.201 5.838l-2.028-2.028A4.5 4.5 0 018.19 9.604L5.935 7.35zm6.979 6.978l-3.242-3.242a2.5 2.5 0 003.241 3.241zm7.893 2.264l-1.431-1.43A8.935 8.935 0 0020.777 12 9.005 9.005 0 009.552 5.338L7.974 3.76C9.221 3.27 10.58 3 12 3c5.392 0 9.878 3.88 10.819 9a10.947 10.947 0 01-2.012 4.592zm-9.084-9.084a4.5 4.5 0 014.769 4.769l-4.77-4.769z"
)

export const RiMailForbidLine = remixIcon(
  "ri-mail-forbid-line",
  "M20 7.238l-7.928 7.1L4 7.216V19h7.07a6.95 6.95 0 00.604 2H3a1 1 0 01-1-1V4a1 1 0 011-1h18a1 1 0 011 1v8.255a6.972 6.972 0 00-2-.965V7.238zM19.501 5H4.511l7.55 6.662L19.502 5zm-2.794 15.708a3 3 0 004.001-4.001l-4.001 4zm-1.415-1.415l4.001-4a3 3 0 00-4.001 4.001zM18 23a5 5 0 110-10 5 5 0 010 10z"
)

export const RiShieldUserLine = remixIcon(
  "ri-shield-user-line",
  "M3.783 2.826L12 1l8.217 1.826a1 1 0 01.783.976v9.987a6 6 0 01-2.672 4.992L12 23l-6.328-4.219A6 6 0 013 13.79V3.802a1 1 0 01.783-.976zM5 4.604v9.185a4 4 0 001.781 3.328L12 20.597l5.219-3.48A4 4 0 0019 13.79V4.604L12 3.05 5 4.604zM12 11a2.5 2.5 0 110-5 2.5 2.5 0 010 5zm-4.473 5a4.5 4.5 0 018.946 0H7.527z"
)

export const RiUserUnfollowLine = remixIcon(
  "ri-user-unfollow-line",
  "M14 14.252v2.09A6 6 0 006 22l-2-.001a8 8 0 0110-7.748zM12 13c-3.315 0-6-2.685-6-6s2.685-6 6-6 6 2.685 6 6-2.685 6-6 6zm0-2c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm7 6.586l2.121-2.122 1.415 1.415L20.414 19l2.122 2.121-1.415 1.415L19 20.414l-2.121 2.122-1.415-1.415L17.586 19l-2.122-2.121 1.415-1.415L19 17.586z"
)

export const RiErrorWarningLine = remixIcon(
  "ri-error-warning-line",
  "M12 22C6.477 22 2 17.523 2 12S6.477 2 12 2s10 4.477 10 10-4.477 10-10 10zm0-2a8 8 0 100-16 8 8 0 000 16zm-1-5h2v2h-2v-2zm0-8h2v6h-2V7z"
)

export const RiBriefcaseLine = remixIcon(
  "ri-briefcase-line",
  "M7 5V2a1 1 0 011-1h8a1 1 0 011 1v3h4a1 1 0 011 1v14a1 1 0 01-1 1H3a1 1 0 01-1-1V6a1 1 0 011-1h4zM4 16v3h16v-3H4zm0-2h16V7H4v7zM9 3v2h6V3H9zm2 8h2v2h-2v-2z"
)

export const RiKey2Line = remixIcon(
  "ri-key-2-line",
  "M10.758 11.828l7.849-7.849 1.414 1.414-1.414 1.415 2.474 2.474-1.414 1.415-2.475-2.475-1.414 1.414 2.121 2.121-1.414 1.415-2.121-2.122-2.192 2.192a5.002 5.002 0 01-7.708 6.294 5 5 0 016.294-7.708zm-.637 6.293A3 3 0 105.88 13.88a3 3 0 004.242 4.242z"
)

export const RiArrowGoBackFill = remixIcon(
  "ri-arrow-go-back-fill",
  "M8 7v4L2 6l6-5v4h5a8 8 0 110 16H4v-2h9a6 6 0 100-12H8z"
)
export const RiPencilFill = remixIcon(
  "ri-pencil-fill",
  "M12.9 6.858l4.242 4.243L7.242 21H3v-4.243l9.9-9.9zm1.414-1.414l2.121-2.122a1 1 0 011.414 0l2.829 2.829a1 1 0 010 1.414l-2.122 2.121-4.242-4.242z"
)
export const RiTimeFill = remixIcon(
  "ri-time-fill",
  'M12 22C6.477 22 2 17.523 2 12S6.477 2 12 2s10 4.477 10 10-4.477 10-10 10zm1-10V7h-2v7h6v-2h-4z"/>'
)
export const RiErrorWarningFill = remixIcon(
  "ri-error-warning-fill",
  "M12 22C6.477 22 2 17.523 2 12S6.477 2 12 2s10 4.477 10 10-4.477 10-10 10zm-1-7v2h2v-2h-2zm0-8v6h2V7h-2z"
)
export const RiCloseFill = remixIcon(
  "ri-close-fill",
  "M12 10.586l4.95-4.95 1.414 1.414-4.95 4.95 4.95 4.95-1.414 1.414-4.95-4.95-4.95 4.95-1.414-1.414 4.95-4.95-4.95-4.95L7.05 5.636z"
)
export const RiCheckFill = remixIcon(
  "ri-check-fill",
  "M10 15.172l9.192-9.193 1.415 1.414L10 18l-6.364-6.364 1.414-1.414z"
)
export const RiMailCheckFill = remixIcon(
  "ri-mail-check-fill",
  "M22 13.341A6 6 0 0014.341 21H3a1 1 0 01-1-1V4a1 1 0 011-1h18a1 1 0 011 1v9.341zm-9.94-1.658L5.648 6.238 4.353 7.762l7.72 6.555 7.581-6.56-1.308-1.513-6.285 5.439zM19 22l-3.536-3.536 1.415-1.414L19 19.172l3.536-3.536 1.414 1.414L19 22z"
)
export const RiHome2Fill = remixIcon(
  "ri-home-2-fill",
  "M20 20a1 1 0 01-1 1H5a1 1 0 01-1-1v-9H1l10.327-9.388a1 1 0 011.346 0L23 11h-3v9z"
)
export const RiMailAddLine = remixIcon(
  "ri-mail-add-line",
  "M22 13h-2V7.238l-7.928 7.1L4 7.216V19h10v2H3a1 1 0 01-1-1V4a1 1 0 011-1h18a1 1 0 011 1v9zM4.511 5l7.55 6.662L19.502 5H4.511zM21 18h3v2h-3v3h-2v-3h-3v-2h3v-3h2v3z"
)

export const RiUserFollowLine = remixIcon(
  "ri-user-follow-line",
  "M14 14.252v2.09A6 6 0 006 22l-2-.001a8 8 0 0110-7.748zM12 13c-3.315 0-6-2.685-6-6s2.685-6 6-6 6 2.685 6 6-2.685 6-6 6zm0-2c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm5.793 8.914l3.535-3.535 1.415 1.414-4.95 4.95-3.536-3.536 1.415-1.414 2.12 2.121z"
)

export const RiUserFill = remixIcon(
  "ri-user-fill",
  "M4 22a8 8 0 1116 0H4zm8-9c-3.315 0-6-2.685-6-6s2.685-6 6-6 6 2.685 6 6-2.685 6-6 6z"
)

export const RiCloseCircleLine = remixIcon(
  "ri-close-circle-line",
  "M12 22C6.477 22 2 17.523 2 12S6.477 2 12 2s10 4.477 10 10-4.477 10-10 10zm0-2a8 8 0 100-16 8 8 0 000 16zm0-9.414l2.828-2.829 1.415 1.415L13.414 12l2.829 2.828-1.415 1.415L12 13.414l-2.828 2.829-1.415-1.415L10.586 12 7.757 9.172l1.415-1.415L12 10.586z"
)

export const RiCloseCircleFill = remixIcon(
  "ri-close-circle-fill",
  "M12 22C6.477 22 2 17.523 2 12S6.477 2 12 2s10 4.477 10 10-4.477 10-10 10zm0-11.414L9.172 7.757 7.757 9.172 10.586 12l-2.829 2.828 1.415 1.415L12 13.414l2.828 2.829 1.415-1.415L13.414 12l2.829-2.828-1.415-1.415L12 10.586z"
)

export const RiQuestionLine = remixIcon(
  "ri-question-line",
  "M12 22C6.477 22 2 17.523 2 12S6.477 2 12 2s10 4.477 10 10-4.477 10-10 10zm0-2a8 8 0 100-16 8 8 0 000 16zm-1-5h2v2h-2v-2zm2-1.645V14h-2v-1.5a1 1 0 011-1 1.5 1.5 0 10-1.471-1.794l-1.962-.393A3.501 3.501 0 1113 13.355z"
)

export const RiAddCircleLine = remixIcon(
  "ri-add-circle-line",
  "M11 11V7h2v4h4v2h-4v4h-2v-4H7v-2h4zm1 11C6.477 22 2 17.523 2 12S6.477 2 12 2s10 4.477 10 10-4.477 10-10 10zm0-2a8 8 0 100-16 8 8 0 000 16z"
)

export const RiChat3Line = remixIcon(
  "ri-chat-3-line",
  "M7.291 20.824L2 22l1.176-5.291A9.956 9.956 0 012 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10a9.956 9.956 0 01-4.709-1.176zm.29-2.113l.653.35A7.955 7.955 0 0012 20a8 8 0 10-8-8c0 1.334.325 2.618.94 3.766l.349.653-.655 2.947 2.947-.655z"
)

export const RiUserSettingsLine = remixIcon(
  "ri-user-settings-line",
  "M12 14v2a6 6 0 00-6 6H4a8 8 0 018-8zm0-1c-3.315 0-6-2.685-6-6s2.685-6 6-6 6 2.685 6 6-2.685 6-6 6zm0-2c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm2.595 7.812a3.51 3.51 0 010-1.623l-.992-.573 1-1.732.992.573A3.496 3.496 0 0117 14.645V13.5h2v1.145c.532.158 1.012.44 1.405.812l.992-.573 1 1.732-.992.573a3.51 3.51 0 010 1.622l.992.573-1 1.732-.992-.573a3.496 3.496 0 01-1.405.812V22.5h-2v-1.145a3.496 3.496 0 01-1.405-.812l-.992.573-1-1.732.992-.572zM18 19.5a1.5 1.5 0 100-3 1.5 1.5 0 000 3z"
)

export const RiUserLine = remixIcon(
  "ri-user-line",
  "M4 22a8 8 0 1116 0h-2a6 6 0 10-12 0H4zm8-9c-3.315 0-6-2.685-6-6s2.685-6 6-6 6 2.685 6 6-2.685 6-6 6zm0-2c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4z"
)

export const RiUserAddLine = remixIcon(
  "ri-user-add-line",
  "M14 14.252v2.09A6 6 0 006 22l-2-.001a8 8 0 0110-7.748zM12 13c-3.315 0-6-2.685-6-6s2.685-6 6-6 6 2.685 6 6-2.685 6-6 6zm0-2c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm6 6v-3h2v3h3v2h-3v3h-2v-3h-3v-2h3z"
)

export const RiSurveyFill = remixIcon(
  "ri-survey-fill",
  "M6 4v4h12V4h2.007c.548 0 .993.445.993.993v16.014a.994.994 0 01-.993.993H3.993A.994.994 0 013 21.007V4.993C3 4.445 3.445 4 3.993 4H6zm3 13H7v2h2v-2zm0-3H7v2h2v-2zm0-3H7v2h2v-2zm7-9v4H8V2h8z"
)

export const RiEditLine = remixIcon(
  "ri-edit-line",
  "M6.414 16L16.556 5.858l-1.414-1.414L5 14.586V16h1.414zm.829 2H3v-4.243L14.435 2.322a1 1 0 011.414 0l2.829 2.829a1 1 0 010 1.414L7.243 18zM3 20h18v2H3v-2z"
)

export const RiChatDownloadLine = remixIcon(
  "ri-chat-download-line",
  "M6.455 19L2 22.5V4a1 1 0 011-1h18a1 1 0 011 1v14a1 1 0 01-1 1H6.455zM4 18.385L5.763 17H20V5H4v13.385zM13 11h3l-4 4-4-4h3V7h2v4z"
)

export const RiChatUploadLine = remixIcon(
  "ri-chat-upload-line",
  "M6.455 19L2 22.5V4a1 1 0 011-1h18a1 1 0 011 1v14a1 1 0 01-1 1H6.455zM4 18.385L5.763 17H20V5H4v13.385zM13 11v4h-2v-4H8l4-4 4 4h-3z"
)

export const RiCheckboxCircleFill = remixIcon(
  "ri-checkbox-circle-fill",
  "M12 22C6.477 22 2 17.523 2 12S6.477 2 12 2s10 4.477 10 10-4.477 10-10 10zm-.997-6l7.07-7.071-1.414-1.414-5.656 5.657-2.829-2.829-1.414 1.414L11.003 16z"
)

export const RiTodoFill = remixIcon(
  "ri-todo-fill",
  "M17 2h3a1 1 0 011 1v18a1 1 0 01-1 1H4a1 1 0 01-1-1V3a1 1 0 011-1h3V0h2v2h6V0h2v2zM7 8v2h10V8H7zm0 4v2h10v-2H7z"
)

export const RiFileSearchFill = remixIcon(
  "ri-file-search-fill",
  "M16 2l5 5v14.008a.993.993 0 01-.993.992H3.993A1 1 0 013 21.008V2.992C3 2.444 3.445 2 3.993 2H16zm-2.471 12.446l2.21 2.21 1.415-1.413-2.21-2.21a4.002 4.002 0 00-6.276-4.861 4 4 0 004.861 6.274zm-.618-2.032a2 2 0 11-2.828-2.828 2 2 0 012.828 2.828z"
)

export const RiSurveyLine = remixIcon(
  "ri-survey-line",
  "M17 2v2h3.007c.548 0 .993.445.993.993v16.014a.994.994 0 01-.993.993H3.993A.994.994 0 013 21.007V4.993C3 4.445 3.445 4 3.993 4H7V2h10zM7 6H5v14h14V6h-2v2H7V6zm2 10v2H7v-2h2zm0-3v2H7v-2h2zm0-3v2H7v-2h2zm6-6H9v2h6V4z"
)

export const RiMailSendLine = remixIcon(
  "ri-mail-send-line",
  "M22 20.007a1 1 0 01-.992.993H2.992A.993.993 0 012 20.007V19h18V7.3l-8 7.2-10-9V4a1 1 0 011-1h18a1 1 0 011 1v16.007zM4.434 5L12 11.81 19.566 5H4.434zM0 15h8v2H0v-2zm0-5h5v2H0v-2z"
)

export const RiChat4Line = remixIcon(
  "ri-chat-4-line",
  "M5.763 17H20V5H4v13.385L5.763 17zm.692 2L2 22.5V4a1 1 0 011-1h18a1 1 0 011 1v14a1 1 0 01-1 1H6.455z"
)

export const RiChatOffLine = {
  name: "ri-chat-off-line",
  minX: 0,
  minY: 0,
  width: 24,
  height: 24,
  raw: '<path fill="none" d="M0 0h24v24H0z"/><path d="M2.808 1.393l19.799 19.8-1.415 1.414-3.608-3.608L6.455 19 2 22.5V4c0-.17.042-.329.116-.469l-.723-.723 1.415-1.415zm1.191 4.02L4 18.385 5.763 17h9.821L4 5.412zM21 3a1 1 0 011 1v13.785l-2-2V5L9.213 4.999 7.214 3H21z"/>',
}

export const RiFileSearchLine = {
  name: "ri-file-search-line",
  minX: 0,
  minY: 0,
  width: 24,
  height: 24,
  raw: '<path fill="none" d="M0 0h24v24H0z"/><path d="M15 4H5v16h14V8h-4V4zM3 2.992C3 2.444 3.447 2 3.999 2H16l5 5v13.993A1 1 0 0120.007 22H3.993A1 1 0 013 21.008V2.992zm10.529 11.454a4.002 4.002 0 01-4.86-6.274 4 4 0 016.274 4.86l2.21 2.21-1.414 1.415-2.21-2.21zm-.618-2.032a2 2 0 10-2.828-2.828 2 2 0 002.828 2.828z"/>',
}

export const RiDeleteBinLine = {
  name: "ri-delete-bin-line",
  minX: 0,
  minY: 0,
  width: 24,
  height: 24,
  raw: '<path fill="none" d="M0 0h24v24H0z"/><path d="M17 6h5v2h-2v13a1 1 0 01-1 1H5a1 1 0 01-1-1V8H2V6h5V3a1 1 0 011-1h8a1 1 0 011 1v3zm1 2H6v12h12V8zm-9 3h2v6H9v-6zm4 0h2v6h-2v-6zM9 4v2h6V4H9z"/>',
}
