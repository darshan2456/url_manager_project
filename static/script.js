document.addEventListener('DOMContentLoaded', function() {
		const tagButtons = document.querySelectorAll('.tag-btn');
    const selectedTagsInput = document.getElementById('selected-tags');
    const selectedTagsDisplay = document.getElementById('selected-tags-display');
    
    tagButtons.forEach(button => {
        button.addEventListener('click', function() {
            const tag = this.getAttribute('data-tag');
            
            // Toggle selection
            this.classList.toggle('selected');
            
            // Update hidden input
            const currentTags = selectedTagsInput.value ? selectedTagsInput.value.split(',') : [];
            if (this.classList.contains('selected')) {
                currentTags.push(tag);
            } else {
                const index = currentTags.indexOf(tag);
                if (index > -1) currentTags.splice(index, 1);
            }
            
            selectedTagsInput.value = currentTags.join(',');
            
            // Update display
            updateSelectedTagsDisplay(currentTags);
        });
    });
    
    function updateSelectedTagsDisplay(tags) {
        selectedTagsDisplay.innerHTML = tags.map(tag => 
            `<span class="selected-tag-pill tag-${tag}">${tag}</span>`
        ).join('');
    }
});