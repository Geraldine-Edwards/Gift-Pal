document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM fully loaded'); // Check if the DOM is ready

const giftContainer = document.querySelector('.gift-container');
const lid = document.querySelector('.lid');
const giftBox = document.querySelector('.gift-box');
const shadow = document.querySelector('.shadow');
const surprise = document.querySelector('.surprise');
const text = document.querySelector('.text');

console.log ('Javascript running');

giftContainer.addEventListener('click', () => {

    console.log('Gift container clicked');  //check when container is clicked

    const isActive = giftContainer.classList.contains('active');
    giftContainer.classList.toggle('active', !isActive);
    lid.classList.toggle('active', !isActive);
    giftBox.classList.toggle('active', !isActive);
    shadow.classList.toggle('active', !isActive);
    surprise.classList.toggle('active', !isActive);
    text.classList.toggle('active', !isActive);
    });
});