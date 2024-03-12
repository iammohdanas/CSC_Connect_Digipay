document.querySelectorAll('.withdraw-btn').forEach(button => {
    button.addEventListener('click', function() {
        document.getElementById('withdrawformamount').value = this.getAttribute('data-amount');
    });
});