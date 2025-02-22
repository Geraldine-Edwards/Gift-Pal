document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM fully loaded'); // Check if the DOM is ready

    const click = document.querySelector('.gift-container');
    const lid = document.querySelector('.lid');
    const giftBox = document.querySelector('.gift-box');
    const shadow = document.querySelector('.shadow');
    const surprise = document.querySelector('.surprise');
    const text = document.querySelector('.text');

    console.log ('Javascript running');

    click.addEventListener('click', () => {
        console.log('Gift container clicked');
        if (click.className === "gift-container") {
            click.classList.add('active');
            lid.classList.add('active');
            giftBox.classList.add('active');
            shadow.classList.add('active');
            surprise.classList.add('active');
            text.classList.add('active');
        } else {
            click.classList.remove('active');
            lid.classList.remove('active');
            giftBox.classList.remove('active');
            shadow.classList.remove('active');
            surprise.classList.remove('active');
            text.classList.remove('active');
        }
    });
});