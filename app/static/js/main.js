
//10초마다 날씨 데이터 자동 업데이트하는 함수
async function updateWeather(){
    console.log("⏳ updateWeather() 실행됨!");

    try{
        let response = await fetch(window.location.href);
        let text = await response.text();

        let parser = new DOMParser();
        let newDoc = parser.parseFromString(text, "text/html");

        document.getElementById("weatherIcon").src = newDoc.getElementById("weatherIcon").src;
        document.getElementById("temperature").innerText = newDoc.getElementById("temperature").innerText;
        document.getElementById("humidity").innerText = newDoc.getElementById("humidity").innerText;
        document.getElementById("wind").innerText = newDoc.getElementById("wind").innerText;
        document.getElementById("description").innerText = newDoc.getElementById("description").innerText;

        console.log("✅ 업데이트 완료! 새로운 온도:", newDoc.getElementById("temperature").innerText);            
    } catch (error) {
        console.error("❌ 업데이트 중 오류 발생:",error);
    }
}

    setInterval(updateWeather, 10000);

// 온도에 맞는 추천 룩과 옷 태그 출력하는 함수
function recommendOutfit() {
let temperature = parseFloat(document.getElementById("temperature").innerText);

// 온도별 추천 태그 & 이미지 데이터
let recommendOutfitData = {
    27: {
        tags: ["#민소매 반팔", "#반바지", "#짧은 치마", "#린넨 옷"],
        images: ["images/summer/image1.png","images/summer/image2.png","images/summer/image3.png","images/summer/image4.png"] 
    },
    22: {
        tags: ["#반팔", "#얇은 셔츠", "#반바지", "#면바지"],
        images: ["images/summer/image5.png","images/summer/image6.png","images/summer/image7.png","images/summer/image8.png"]
    },
    19: {
        tags: ["#블라우스", "#긴팔 티", "#면바지", "#슬랙스"],
        images: ["images/autumn/image1.png","images/autumn/image2.png","images/autumn/image3.png","images/autumn/image4.png"]
    },
    16: {
        tags: ["#얇은 가디건", "#얇은 니트", "#맨투맨", "#후드", "#긴바지"],
        images: ["images/spring/image1.png","images/spring/image2.png","images/spring/image3.png","images/spring/image4.png"]
    },
    11: {
        tags: ["#자켓", "#가디건", "#청자켓", "#니트", "#스타킹", "#청바지"],
        images: ["images/spring/image5.png","images/spring/image6.png","images/autumn/image1.png","images/autumn/image2.png"]
    },
    8: {
        tags: ["#트랜치 코트", "#야상", "#점퍼", "#스타킹", "#기모바지"],
        images: ["images/autumn/image3.png","images/autumn/image4.png","images/autumn/image5.png","images/autumn/image6.png"]
    },
    4: {
        tags: ["#울 코트", "#히트텍", "#가죽 옷", "#기모"],
        images: ["images/winter/image1.png","images/winter/image2.png","images/winter/image3.png","images/winter/image4.png"]
    },
    0: {
        tags: ["#패딩", "#두꺼운 코트", "#누빔 옷", "#기모", "#목도리"],
        images: ["images/winter/image5.png", "images/winter/image6.png", "images/winter/image7.png", "images/winter/image8.png"]
    }
};

// 온도별 키 지정
let selectedKey = "";
if (temperature >= 28) selectedKey = 27;
else if (temperature >= 23) selectedKey = 22;
else if (temperature >= 20) selectedKey = 19;
else if (temperature >= 17) selectedKey = 16;
else if (temperature >= 12) selectedKey = 11;
else if (temperature >= 9) selectedKey = 8;
else if (temperature >= 5) selectedKey = 4;
else selectedKey = 0;

let selectedData = recommendOutfitData[selectedKey];

// 추천 태그와 이미지 출력을 위한 리스트 요소 가져오기
let listElement = document.getElementById("outfitList");

// 기존 내용 초기화 (새로운 데이터로 업데이트 전에 기존 내용 비우기)
listElement.innerHTML = ""; 

// selectedData (온도에 맞는 추천 데이터)가 있는지 확인
if (selectedData) {
    // 새로운 div 요소 생성 (전체 outfit 아이템을 감싸는 컨테이너)
    let div = document.createElement("div");
    div.classList.add("outfit-item"); // div에 'outfit-item' 클래스를 추가 (스타일링을 위해)

    // 태그 영역을 위한 div 생성
    let tagDiv = document.createElement("div");
    tagDiv.classList.add("tags"); // 'tags' 클래스를 추가해서 스타일을 적용

    // 개선된 방식: 각 태그를 개별 <span> 요소로 생성
    selectedData.tags.forEach(tag => {
        let tagSpan = document.createElement("span");
        tagSpan.classList.add("tag");  // CSS에서 이 클래스에 원하는 스타일을 적용
        tagSpan.textContent = tag;
        tagDiv.appendChild(tagSpan);
    });


    // 태그 영역 div를 전체 outfit div에 추가
    div.appendChild(tagDiv);

    // 이미지 영역을 위한 div 생성
    let imageDiv = document.createElement("div");
    imageDiv.classList.add("images"); // 'images' 클래스를 추가해서 스타일을 적용

    // 이미지 데이터를 최대 4개까지 처리해서 이미지 태그 생성
    selectedData.images.slice(0, 4).forEach(imageSrc => {
        let img = document.createElement("img"); // 새로운 이미지 요소 생성
        img.src = `/static/${imageSrc}`; // 이미지 파일 경로 설정
        img.alt = "추천 룩"; // 이미지 설명 추가 (대체 텍스트)
        
        imageDiv.appendChild(img); // 이미지를 이미지 영역 div에 추가
    });

    // 이미지 영역 div를 전체 outfit div에 추가
    div.appendChild(imageDiv);

    // outfit 아이템을 outfit list에 추가
    listElement.appendChild(div);
}

}

// 페이지 로드 시 실행
window.onload = recommendOutfit;


