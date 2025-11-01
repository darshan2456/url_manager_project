document.addEventListener('DOMContentLoaded', function() {
    // Tag selection functionality for the form
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

    // Dropdown functionality for tag sidebar
    const tagSidebarButtons = document.querySelectorAll('.tag-sidebar-btn');
    
    tagSidebarButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.stopPropagation();
            const tag = this.getAttribute('data-tag');
            toggleDropdown(tag);
        });
    });

    // Copy URL functionality - ONLY for saved URLs (not archived)
    const copyButtons = document.querySelectorAll('.url-item:not(.archived) .copy-btn');
    
    copyButtons.forEach(button => {
        button.addEventListener('click', async function() {
            const url = this.getAttribute('data-url');
            
            try {
                await navigator.clipboard.writeText(url);
                
                // Visual feedback
                this.classList.add('copied');
                this.textContent = 'Copied!';
                
                // Reset after 2 seconds
                setTimeout(() => {
                    this.classList.remove('copied');
                    this.textContent = 'Copy URL';
                }, 2000);
                
            } catch (err) {
                // Fallback for older browsers
                console.error('Failed to copy: ', err);
                alert('Failed to copy URL to clipboard');
            }
        });
    });

    // Close dropdowns when clicking outside
    document.addEventListener('click', function() {
        closeAllDropdowns();
    });
});

function toggleDropdown(tag) {
    const dropdown = document.getElementById('dropdown-' + tag);
    const isCurrentlyOpen = dropdown.style.display === 'block';
    
    // Close all dropdowns first
    closeAllDropdowns();
    
    // If it wasn't open, open this one
    if (!isCurrentlyOpen) {
        dropdown.style.display = 'block';
    }
}

function closeAllDropdowns() {
    const allDropdowns = document.querySelectorAll('.tag-dropdown');
    allDropdowns.forEach(dropdown => {
        dropdown.style.display = 'none';
    });
}