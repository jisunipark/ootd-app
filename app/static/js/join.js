document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("joinForm");

  form.addEventListener("submit", function (event) {
    // 이름, 닉네임, 아이디, 비밀번호, 이메일, 성별 검사
    const name = document.getElementById("name");
    const nickname = document.getElementById("nickname");
    const username = document.getElementById("username");
    const password = document.getElementById("password");
    const email = document.getElementById("email");
    const gender = document.querySelector('input[name="gender"]:checked');

    let isValid = true;
    let errorMessages = [];

    // 이름 검사 (2~7자)
    if (name.value.length < 2 || name.value.length > 7) {
      isValid = false;
      errorMessages.push("이름은 2자 이상 7자 이하로 입력해주세요.");
    }

    // 닉네임 검사 (최대 10자)
    if (nickname.value.length > 10) {
      isValid = false;
      errorMessages.push("닉네임은 2자 이상 10자 이하로 입력해주세요.");
    }

    // 아이디 검사 (최대 20자)
    if (username.value.length > 20) {
      isValid = false;
      errorMessages.push("아이디는 7자 이상 20자 이하로 입력해주세요.");
    }

    // 비밀번호 검사 (최대 20자)
    if (password.value.length > 20) {
      isValid = false;
      errorMessages.push("비밀번호는 7자 이상 20자 이하로 입력해주세요.");
    }

    // 이메일 검사
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (!emailPattern.test(email.value)) {
      isValid = false;
      errorMessages.push("이메일 형식이 올바르지 않습니다. 이메일에 '@'를 포함시켜 입력해주세요.");
    }

    // 성별 선택 검사
    if (!gender) {
      isValid = false;
      errorMessages.push("성별을 선택해주세요.");
    }

    // 오류 메시지 표시
    const errorContainer = document.getElementById("errorMessages");
    errorContainer.innerHTML = "";

    if (!isValid) {
      event.preventDefault(); // 폼 제출 막기
      errorMessages.forEach(function (message) {
        const errorMessageElement = document.createElement("p");
        errorMessageElement.textContent = message;
        errorContainer.appendChild(errorMessageElement);
      });
    }
  });
});
