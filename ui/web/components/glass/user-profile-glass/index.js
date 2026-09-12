const btnFollow = document.getElementById('btnFollow');
const followText = document.getElementById('followText');
const followIcon = document.getElementById('followIcon');
const followerCount = document.getElementById('followerCount');

let isFollowing = false;

btnFollow.addEventListener('click', () => {
    isFollowing = !isFollowing;
    btnFollow.classList.toggle('following', isFollowing);
    if (isFollowing) {
        followText.textContent = 'Following';
        followIcon.setAttribute('data-lucide', 'check');
        followerCount.textContent = '14.9k';
    } else {
        followText.textContent = 'Follow';
        followIcon.setAttribute('data-lucide', 'user-plus');
        followerCount.textContent = '14.8k';
    }
    if (window.lucide) lucide.createIcons();
});