const Conts = document.getElementsByClassName('Cont');

function toggleContent(element) {
  const next = element.nextElementSibling;

  document.querySelectorAll('.Cont-Details.open').forEach(div => {
    if (div !== next) div.classList.remove('open');
  });

  if (next && next.classList.contains('Cont-Details')) {
    next.classList.toggle('open');
  }
}


