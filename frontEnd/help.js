//* Elements
let serverSection = document.getElementById("pi-help");
let databaseSection = document.getElementById("db-help");
let frontEndSection = document.getElementById("front-end-help");
let troubleshootingSection = document.getElementById("troubleshooting");

//* Functions
function smoothScroll(location) {
  switch (location) {
    case "server":
      serverSection.scrollIntoView({
        block: "start",
        behavior: "smooth",
        inline: "start",
      });
      break;

    case "database":
      databaseSection.scrollIntoView({
        block: "start",
        behavior: "smooth",
        inline: "start",
      });
      break;

    case "front":
      frontEndSection.scrollIntoView({
        block: "start",
        behavior: "smooth",
        inline: "start",
      });
      break;

    case "npm":
      document.getElementById("npm-start").scrollIntoView({
        block: "start",
        behavior: "smooth",
        inline: "start",
      });
      break;

    case "ifconfig":
      document.getElementById("ifconfig").scrollIntoView({
        block: "start",
        behavior: "smooth",
        inline: "start",
      });
      break;

    case "troubleshooting":
      document.getElementById("troubleshooting").scrollIntoView({
        block: "start",
        behavior: "smooth",
        inline: "start",
      });
      break;

    case "toc":
      window.scroll({
        top: 0,
        left: 0,
        behavior: "smooth",
      });
      break;

    case "test":
      console.log("test scroll");
      break;
  }
}
