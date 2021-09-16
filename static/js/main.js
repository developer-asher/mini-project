const body = document.querySelector('body');
const campingWrap = document.querySelector('.camping');
let SORT_NUM = 30;

function createCampingListTemp(ele, len) {
  campingWrap.innerHTML = ``;
  len = len > SORT_NUM ? SORT_NUM : len;

  for (let i = 0; i < len; i++) {
    const img = ele[i].img;
    const tag = ele[i].tag;
    const name = ele[i].name;
    const loc = ele[i].location;
    const view = ele[i].view;
    const gourl = ele[i].gourl;
    const article_temp = `
                  <article class="review__popUp">
                      <div>
                        <i></i>
                        <p class="review__question">
                          해당 캠핑장에 대해 어떻게 생각하시나요?
                        </p>
                      </div>
                      <table class="review__tb">
                        <thead>
                          <tr>
                            <th class="review__author">작성자</th>
                            <th class="review__comment">코멘트</th>
                            <th class="review__star">평점</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr>
                            <td>조성민</td>
                            <td>좋습니다</td>
                            <td>4.6점</td>
                          </tr>
                        </tbody>
                      </table>
                      <footer class="ft__review">
                        <form class="review__form">
                          <p class="form__desc">별점과 이용후기를 남겨주세요.</p>
                          <p class="form__star">
                            <button class="star">
                              <i class="fas fa-star star_1"></i>
                            </button>
                            <button class="star">
                              <i class="fas fa-star star_2"></i>
                            </button>
                            <button class="star">
                              <i class="fas fa-star star_3"></i>
                            </button>
                            <button class="star">
                              <i class="fas fa-star star_4"></i>
                            </button>
                            <button class="star">
                              <i class="fas fa-star star_5"></i>
                            </button>
                          </p>
                          <p class="form__text">
                            <label for="write"></label>
                            <textarea
                              name=""
                              id="write"
                              cols="30"
                              rows="6"
                            ></textarea>
                          </p>
                          <button class="form__register">등록</button>
                        </form>
                      </footer>
                      <button class="btn__close">
                        <i class="fas fa-times"></i>
                      </button>
                    </article>
              `;
    const temp = `
                  <li class="camping__list clear">
                      <img
                          src="${img}"
                          alt="${name}"
                          class="camping__img"
                        />
                      <div class="camping__info">
                          <div class="camping__desc">
                              <p class="camping__tag">
                                ${
                                  tag
                                    ? `<span class="tab__title">연관태그</span>: <span class="tag__name">${tag}</span>`
                                    : '연관태그: 해당없음'
                                }
                              </p>
                              <p class="camping__name">${name}</p>
                              <p class="camping__loc">${loc}</p>
                          </div>
                          <div>
                              <a class="camping__link" href="${gourl}" target="_blank">바로가기</a>
                              <button class="camping__review">리뷰작성</button>
                              <span class="camping__view">조회수 : ${view}</span>
                          </div>
                      </div>
                      <div class="article__bg modal">
                          ${article_temp}
                      </div>
                  </li>
              `;
    campingWrap.innerHTML += temp;
  }
}

function openModal(ele) {
  const campingInfo = ele.parentElement.parentElement;
  const targetModal = campingInfo.nextElementSibling;

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

  banner.style.width = `${(BANNER_COUNT + 1) * 100}%`;
  bannerLists.forEach((list) => {
    list.style.width = `${100 / (BANNER_COUNT + 1)}%`;
  });

  setInterval(() => {
    if (curIdx <= 2) {
      banner.style.transform = `translateX(-${
        bannerListWidth * (curIdx + 1)
      }px)`;
      banner.style.transition = `transform 1s ease-out`;
    }

    if (curIdx === 2) {
      setTimeout(() => {
        banner.style.transform = `translateX(0)`;
        banner.style.transition = 'transform 0s ease-out';
      }, 1000);
      curIdx = -1;
    }

    curIdx++;
  }, 2000);
}

function getCampingList() {
  campingWrap.innerHTML = ``;

  $.ajax({
    type: 'GET',
    url: '/camping',
    data: {},
    success: function (response) {
      const campInfos = response.campInfos;

      createCampingListTemp(campInfos, 30);
    },
  });

  campingWrap.addEventListener('click', (event) => {
    const reviewStarWrap = campingWrap.querySelector('.form__star');
    const reviewRegister = campingWrap.querySelector('.form__register');
    const reviewComment = campingWrap.querySelector('#write');
    const target = event.target;

    event.preventDefault();

    if (target.tagName !== 'I') {
      return false;
    }
    printStar(target);

    const star = reviewStarWrap.querySelectorAll('.star.on').length;
    const comment = reviewComment.value;

    $.ajax({
      type: 'POST',
      url: '/review',
      data: { review_star: star, review_comment: comment },
      success: function (response) {
        console.log(response);
      },
    });
  });
}

function loadView() {}

function printStar(target) {
  const parents = target.parentElement.parentElement;
  const nthStar = parents.querySelectorAll('.star > i');

  nthStar.forEach((item) => {
    item.parentElement.classList.remove('on');
  });

  const stars = target.className.split('_')[1];
  for (let i = 0; i < stars; i++) {
    nthStar[i].parentElement.classList.add('on');
  }
}

function setSortEvent() {
  const sortLoc = document.querySelector('#sort_loc');
  const sortView = document.querySelector('#sort_view');
  const sortTheme = document.querySelector('#sort_theme');
  let descending = true;

  sortLoc.addEventListener('change', (event) => {
    event.preventDefault();
    const city = event.target.value;

    $.ajax({
      type: 'POST',
      url: '/sort_city',
      data: { loc: city },
      success: function (response) {
        const sort_city = response.sort_city;

        if (sort_city.length <= 0) {
          alert('해당 지역에 관한 캠핑장이 없습니다.');
          return false;
        }
        createCampingListTemp(sort_city, sort_city.length);
      },
    });
  });

  sortTheme.addEventListener('change', (event) => {
    event.preventDefault();
    const theme = event.target.value;

    $.ajax({
      type: 'POST',
      url: '/sort_theme',
      data: { theme: theme },
      success: function (response) {
        const sort_theme = response.sort_theme;

        createCampingListTemp(sort_theme, sort_theme.length);
      },
    });
  });

  sortView.addEventListener('click', (event) => {
    event.preventDefault();
    if (descending) {
      order = 'descending';
      descending = false;
    } else {
      order = 'ascending';
      descending = true;
    }

    $.ajax({
      type: 'POST',
      url: '/sort_order',
      data: { order: order },
      success: function (response) {
        const sort_order = response.sort_order;

        createCampingListTemp(sort_order, sort_order.length);
      },
    });
  });
}
// sort event
setSortEvent();

window.addEventListener('load', () => {
  getCampingList();
  createBanner();
});

campingWrap.addEventListener('click', (event) => {
  const target = event.target;

  if (target.className !== 'camping__review') {
    return false;
  }

  openModal(target);
});
