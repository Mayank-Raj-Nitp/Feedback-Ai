// Add click handler for language selector
document.querySelector('.language-selector').addEventListener('click', function(e) {
    e.stopPropagation();
    this.querySelector('.language-dropdown').style.display = 
        this.querySelector('.language-dropdown').style.display === 'block' ? 'none' : 'block';
});

// Close dropdown when clicking outside
document.addEventListener('click', function() {
    document.querySelector('.language-dropdown').style.display = 'none';
});

 // Show/hide back to top button
 window.onscroll = function() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        document.getElementById("backToTop").style.display = "block";
    } else {
        document.getElementById("backToTop").style.display = "none";
    }
};

// Scroll to top function
document.getElementById("backToTop").onclick = function() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
};

 // Product data loader
 function loadProduct() {
    const urlParams = new URLSearchParams(window.location.search);
    const productId = urlParams.get('id');
    
    // Sample data - replace with actual product data
    const products = {
        '1': {
            title: "Cotton Jersey Tops",
            price: "1499",
            material: "100% Premium Cotton",
            image: "./assests/tops.jpg"
        },
        // Add other products
    };

    if(products[productId]) {
        document.getElementById('productTitle').textContent = products[productId].title;
        document.getElementById('productPrice').textContent = products[productId].price;
        document.getElementById('materialDetails').textContent = products[productId].material;
        document.getElementById('mainImage').src = products[productId].image;
    }
}

// Review system
let currentRating = 0;

function rateProduct(stars) {
    const starsElements = document.querySelectorAll('#reviewStars i');
    starsElements.forEach((star, index) => {
        star.classList.toggle('bi-star-fill', index < stars);
        star.classList.toggle('bi-star', index >= stars);
    });
    currentRating = stars;
}

function submitReview() {
    const reviewText = document.querySelector('textarea').value;
    // Add your review submission logic here
    alert('Thank you for your review!');
}

// Image gallery
function changeImage(src) {
    document.getElementById('mainImage').src = src;
}

// Initialize page
window.onload = loadProduct;

function toggleLanguageDropdown() {
    const dropdown = document.getElementById('languageDropdown');
    dropdown.style.display = dropdown.style.display === 'none' || dropdown.style.display === '' ? 'block' : 'none';
}
