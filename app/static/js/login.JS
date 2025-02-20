document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("loginForm");

  form.addEventListener("submit", function (event) {
      const username = document.getElementById("username");
      const password = document.getElementById("password");
      const errorContainer = document.getElementById("errorMessages");

      let isValid = true;
      let errorMessages = [];

      errorContainer.innerHTML = "";

      if (username.value.length < 7 || username.value.length > 20) {
          isValid = false;
          errorMessages.push("아이디는 7자 이상 20자 이하로 입력해주세요.");
      }

      if (password.value.length < 7 || password.value.length > 20) {
          isValid = false;
          errorMessages.push("비밀번호는 7자 이상 20자 이하로 입력해주세요.");
      }

      if (!isValid) {
          event.preventDefault();
          errorMessages.forEach(function (message) {
              const errorMessageElement = document.createElement("p");
              errorMessageElement.textContent = message;
              errorContainer.appendChild(errorMessageElement);
          });
      }
  });
});
