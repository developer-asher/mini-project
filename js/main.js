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

camping.addEventListener('click', (event) => {
  const target = event.target;

  if (target.className !== 'camping__review') {
    return false;
  }

  openModal(target);
});

window.addEventListener('load', () => {
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
