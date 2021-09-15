const body = document.querySelector('body');
const camping = document.querySelector('.camping__desc');
const reviewStar = document.querySelector('.form__star');

function openModal(ele) {
    const parent = ele.parentElement;
    const targetModal = parent.nextElementSibling;

    targetModal.classList.add('on');
    body.classList.add('stop__scroll');

    const btnClose = targetModal.querySelector('.btn__close');
    btnClose.addEventListener('click', () => {
        closeModal(targetModal);
    });
}

function closeModal(ele) {
    ele.classList.remove('on');
    body.classList.remove('stop__scroll');
}

function createBanner() {
    const banner = document.querySelector('.banner');
    const bannerLists = document.querySelectorAll('.banner > li');
    const bannerListWidth = bannerLists[0].getBoundingClientRect().width;
    const BANNER_COUNT = bannerLists.length;
    let curIdx = 0;

    const li = document.createElement('li');
    li.classList.add('banner__list4', 'trick__banner');
    li.style.background = `url('../images/camping.jpeg') no-repeat center 80%`;
    li.style.backgroundSize = `cover`;

    banner.appendChild(li);
    banner.style.width = `${(BANNER_COUNT + 1) * 100}%`;
    bannerLists.forEach((list) => {
        list.style.width = `${100 / (BANNER_COUNT + 1)}%`;
    });

    setInterval(() => {
        banner.style.transform = `translateX(-${bannerListWidth * (curIdx + 1)}px)`;
        banner.style.transition = `transform 1s ease-out`;

        curIdx++;

        if (curIdx === 3) {
            setTimeout(() => {
                banner.style.transform = `translateX(0)`;
                banner.style.transition = 'transform 0s ease-out';
            }, 1001);
            curIdx = 0;
        }
    }, 2000);
}

function getCampingList() {
    const campingInfo = document.querySelector('.camping__info');
    campingInfo.innerHTML = ``;
    console.log('캠핑목록 로딩');

    $.ajax({
        type: 'GET',
        url: '/camping',
        data: {},
        success: function (response) {
            const campingInfos = response.campingInfos;
            console.log(campingInfos);
            // campingInfos.forEach(info => {
            //     const img = info.img;
            //     const tag = info.tag;
            //     const name = info.name;
            //     const loc = info.location;
            //     const view = info.view;
            //
            //
            // });
            for (let i = 0; i < 10; i++) {
                const img = campingInfos[i].img;
                const tag = campingInfos[i].tag;
                const name = campingInfos[i].name;
                const loc = campingInfos[i].location;
                const view = campingInfos[i].view;
                const temp = `
                    <img
                        src="${img}"
                        alt="${name}"
                        class="camping__img"
                      />
                    <div class="camping__desc">
                    <p class="camping__tag">
                      연관태그: ${tag}
                    </p>
                    <p class="camping__name">${name}</p>
                    <p class="camping__loc">${loc}</p>
                    </div>
                    <a class="camping__link" href="">바로가기</a>
                    <button class="camping__review">리뷰작성</button>
                    <span class="camping__view">조회수 : ${view}</span>
                `;
                campingInfo.innerHTML += temp;
            }
        }
    })
}

camping.addEventListener('click', (event) => {
    const target = event.target;

    if (target.className !== 'camping__review') {
        return false;
    }

    openModal(target);
});

window.addEventListener('load', () => {
    getCampingList();
    createBanner();
});

reviewStar.addEventListener('click', (event) => {
    const target = event.target;
    event.preventDefault();

    if (target.tagName !== 'I') {
        return false;
    }
    printStar(target);
});

function printStar(target) {
    const nthStar = document.querySelectorAll('.star > i');
    nthStar.forEach((item) => {
        item.parentElement.classList.remove('on');
    });

    const num = target.className.split('_')[1];
    for (let i = 0; i < num; i++) {
        nthStar[i].parentElement.classList.add('on');
    }
}
