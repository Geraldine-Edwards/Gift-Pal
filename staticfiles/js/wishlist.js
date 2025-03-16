document.addEventListener('DOMContentLoaded', function () {
    // Add Category: Handle Form Submission
    document.getElementById('addCategoryForm').addEventListener('submit', function (e) {
        e.preventDefault();
        const formData = new FormData(this);
        const data = {
            name: formData.get('name'),
            occasion_date: formData.get('occasion_date'),
        };

        fetch('/wishlist/api/categories/', {  
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
            },
            body: JSON.stringify(data),
        })
            .then(response => {
                if (!response.ok) {
                    return response.text().then(text => { throw new Error(text) });
                }
                return response.json();
            })
            .then(data => {
                if (data.id) {
                    // Close the modal
                    $('#addCategoryModal').modal('hide');

                    // Clear the form
                    document.getElementById('addCategoryForm').reset();

                    // Get the template
                    const template = document.getElementById('category-template').content;

                    // Clone the template content
                    const newCategory = document.importNode(template, true);

                    // Update the template with the new category's data
                    newCategory.querySelector('.category-name').textContent = data.name;
                    newCategory.querySelector('.category-date').textContent = new Date(data.occasion_date).toLocaleDateString();
                    newCategory.querySelector('.edit-category').dataset.categoryId = data.id;
                    newCategory.querySelector('.edit-category').dataset.categoryName = data.name;
                    newCategory.querySelector('.edit-category').dataset.occasionDate = data.occasion_date;
                    newCategory.querySelector('.delete-category').dataset.categoryId = data.id;

                    // Insert the new category into the page
                    const container = document.querySelector('.container.py-5');
                    container.appendChild(newCategory);
                } else {
                    alert('Error: ' + JSON.stringify(data));
                }
            })
            .catch(error => console.error('Error:', error));
    });

    
    // Set the category ID when the "Add Item" button is clicked
    document.querySelectorAll('[data-bs-target="#addItemModal"]').forEach(button => {
        button.addEventListener('click', function () {
            const categoryId = this.dataset.categoryId; // Get the category ID from the button
            console.log('Category ID:', categoryId); // Debugging: Log the category ID
            document.getElementById('itemCategoryId').value = categoryId; // Set the hidden input value
        });
    });

    // Add Item Form submission
    document.getElementById('addItemForm').addEventListener('submit', function (e) {
        e.preventDefault();
        const formData = new FormData(this);
        const data = {
            category: formData.get('category'),
            item_name: formData.get('item_name'),
            description: formData.get('description'),
            link: formData.get('link'),
            priority: formData.get('priority'),
        };

    
        console.log('Form Data:', data); // Debugging: Log the form data

        fetch('/wishlist/api/items/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
            },
            body: JSON.stringify(data),
        })
            .then(response => response.json())
            .then(data => {
                console.log('Response Data:', data); // Debugging: Log the response data
                if (data.id) {
                    // Close the modal
                    $('#addItemModal').modal('hide');
    
                    // Clear the form
                    document.getElementById('addItemForm').reset();
    
                    // Get the template
                    const template = document.getElementById('item-template').content;
    
                    // Clone the template content
                    const newItem = document.importNode(template, true);
    
                    // Update the template with the new item's data
                    newItem.querySelector('.item-name').textContent = data.item_name;
                    newItem.querySelector('.item-description').textContent = data.description;
                    newItem.querySelector('.item-priority').textContent = data.priority;
                    newItem.querySelector('.edit-item').dataset.itemId = data.id;
                    newItem.querySelector('.delete-item').dataset.itemId = data.id;
    
                    // Insert the new item into the page
                    const container = document.getElementById(`items-container-${data.category}`);
            
                    console.log('Container:', container); // Debugging: Log the container element
            
                    if (container) {
                        container.appendChild(newItem);
                    } else {
                    console.error('Container not found:', `items-container-${data.category}`);
                    }
                } else {
                    alert('Error: ' + JSON.stringify(data));
                }
            })
            .catch(error => console.error('Error:', error));
    });

    // Edit Category: populate Modal
    document.querySelectorAll('.edit-category').forEach(button => {
        button.addEventListener('click', function () {
            const categoryId = this.dataset.categoryId;
            const categoryName = this.dataset.categoryName;
            document.getElementById('editCategoryName').value = categoryName;
            document.getElementById('editCategoryForm').dataset.categoryId = categoryId;
            $('#editCategoryModal').modal('show');
        });
    });

    // Edit Category - handle form submission
    document.getElementById('editCategoryForm').addEventListener('submit', function (e) {
        e.preventDefault();
        const categoryId = this.dataset.categoryId;
        const formData = new FormData(this);
        const data = {
            name: formData.get('name'),
        };

        fetch(`/wishlist/api/categories/${categoryId}/`, {  // Correct URL
            method: 'PUT',  // Use PUT or PATCH for updates
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
            },
            body: JSON.stringify(data),
        })
            .then(response => {
                if (!response.ok) {
                    return response.text().then(text => { throw new Error(text) });
                }
                return response.json();
            })
            .then(data => {
                if (data.id) {
                    // Close the modal
                    $('#editCategoryModal').modal('hide');

                    // Update the category name in the DOM
                    document.getElementById(`category-name-${data.id}`).innerText = data.name;
                } else {
                    alert('Error: ' + JSON.stringify(data));
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error updating category: ' + error.message);
            });
    });

    // Delete Category
    document.querySelectorAll('.delete-category').forEach(button => {
        button.addEventListener('click', function () {
            const categoryId = this.dataset.categoryId;
            if (confirm('Are you sure you want to delete this category?')) {
                fetch(`/wishlist/api/categories/${categoryId}/`, {
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    },
                })
                    .then(response => {
                        if (response.ok) {
                            document.getElementById(`category-${categoryId}`).remove();
                        } else {
                            alert('Error deleting category.');
                        }
                    })
                    .catch(error => console.error('Error:', error));
            }
        });
    });

    // Edit Item
    document.querySelectorAll('.edit-item').forEach(button => {
        button.addEventListener('click', function () {
            const itemId = this.dataset.itemId;
            fetch(`/wishlist/api/items/${itemId}/`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById('editItemName').value = data.item_name;
                    document.getElementById('editItemDescription').value = data.description;
                    document.getElementById('editItemLink').value = data.link;
                    document.getElementById('editItemPriority').value = data.priority;
                    document.getElementById('editItemForm').dataset.itemId = itemId;
                    $('#editItemModal').modal('show');
                });
        });
    });

    // Delete Item
    document.querySelectorAll('.delete-item').forEach(button => {
        button.addEventListener('click', function () {
            const itemId = this.dataset.itemId;
            if (confirm('Are you sure you want to delete this item?')) {
                fetch(`/wishlist/api/items/${itemId}/`, {
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    },
                })
                    .then(response => {
                        if (response.ok) {
                            document.getElementById(`item-${itemId}`).remove();
                        } else {
                            alert('Error deleting item.');
                        }
                    })
                    .catch(error => console.error('Error:', error));
            }
        });
    });
});