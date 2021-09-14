const body = document.querySelector('body');
const camping = document.querySelector('.camping');

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

camping.addEventListener('click', (event) => {
  const target = event.target;
  if (target.className !== 'camping__review') {
    return false;
  }

  openModal(target);
});
