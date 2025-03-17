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

                    // Refresh the page
                    window.location.reload();
                } else {
                    alert('Error: ' + JSON.stringify(data));
                }
            })
            .catch(error => console.error('Error:', error));
    });

    // Set the category ID when the "Add Item" button is clicked
    document.querySelectorAll('[data-bs-target="#addItemModal"]').forEach(button => {
        button.addEventListener('click', function () {
            const categoryId = this.dataset.categoryId;
            console.log('Category ID:', categoryId);
            document.getElementById('itemCategoryId').value = categoryId;
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
                if (data.id) {
                    // Close the modal
                    $('#addItemModal').modal('hide');

                    // Clear the form
                    document.getElementById('addItemForm').reset();

                    // Refresh the page
                    window.location.reload();
                } else {
                    alert('Error: ' + JSON.stringify(data));
                }
            })
            .catch(error => console.error('Error:', error));
    });

    // Edit Category: Populate Modal
    document.querySelectorAll('.edit-category').forEach(button => {
        button.addEventListener('click', function () {
            const categoryId = this.dataset.categoryId;
            const categoryName = this.dataset.categoryName;
            const occasionDate = this.dataset.occasionDate;

            // Debugging: Log the retrieved data
            console.log('Category ID:', categoryId);
            console.log('Category Name:', categoryName);
            console.log('Occasion Date:', occasionDate);

            // Populate the form fields
            document.getElementById('editCategoryName').value = categoryName;
            document.getElementById('editOccasionDate').value = occasionDate;

            // Set the category ID on the form
            document.getElementById('editCategoryForm').dataset.categoryId = categoryId;

            // Show the modal
            $('#editCategoryModal').modal('show');
        });
    });

    // Edit Category: Handle Form Submission
    document.getElementById('editCategoryForm').addEventListener('submit', function (e) {
        e.preventDefault();
        const categoryId = this.dataset.categoryId;
        const formData = new FormData(this);
        const data = {
            name: formData.get('name'),
            occasion_date: formData.get('occasion_date'),
        };

        fetch(`/wishlist/api/categories/${categoryId}/`, {
            method: 'PUT',
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

                    // Refresh the page
                    window.location.reload();
                } else {
                    alert('Error: ' + JSON.stringify(data));
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error updating category: ' + error.message);
            });
    });

    // Delete Category: Show Modal
    document.querySelectorAll('.delete-category').forEach(button => {
        button.addEventListener('click', function () {
            const categoryId = this.dataset.categoryId;

            // Store the category ID in the hidden input
            document.getElementById('deleteCategoryId').value = categoryId;

            // Show the modal
            const deleteCategoryModal = new bootstrap.Modal(document.getElementById('deleteCategoryModal'));
            deleteCategoryModal.show();
        });
    });

    // Move Items to "Uncategorized" and Delete Category
    document.getElementById('moveItemsToUncategorized').addEventListener('click', function () {
        const categoryId = document.getElementById('deleteCategoryId').value;

        if (categoryId) {
            fetch(`/wishlist/api/categories/${categoryId}/move_items_to_uncategorized/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                },
            })
                .then(response => {
                    if (response.ok) {
                        // Close the modal
                        const deleteCategoryModal = bootstrap.Modal.getInstance(document.getElementById('deleteCategoryModal'));
                        deleteCategoryModal.hide();

                        // Refresh the page
                        window.location.reload();
                    } else {
                        alert('Error moving items to "Uncategorized".');
                    }
                })
                .catch(error => console.error('Error:', error));
        }
    });

    // Delete Everything (Category and Items)
    document.getElementById('deleteEverything').addEventListener('click', function () {
        const categoryId = document.getElementById('deleteCategoryId').value;

        if (categoryId) {
            fetch(`/wishlist/api/categories/${categoryId}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                },
            })
                .then(response => {
                    if (response.ok) {
                        // Close the modal
                        const deleteCategoryModal = bootstrap.Modal.getInstance(document.getElementById('deleteCategoryModal'));
                        deleteCategoryModal.hide();

                        // Refresh the page
                        window.location.reload();
                    } else {
                        alert('Error deleting category and items.');
                    }
                })
                .catch(error => console.error('Error:', error));
        }
    });

    // Handle the "X" button and other modal closing events for the Delete Category Modal
    document.getElementById('deleteCategoryModal').addEventListener('hidden.bs.modal', function () {
        console.log('Delete Category Modal closed');
        // Remove the backdrop manually if it persists
        const backdrops = document.querySelectorAll('.modal-backdrop');
        backdrops.forEach(backdrop => backdrop.remove());
        // Optionally, clear the hidden input or reset the state
        document.getElementById('deleteCategoryId').value = '';
    });

    // Edit Item: Populate Modal
    document.querySelectorAll('.edit-item').forEach(button => {
        button.addEventListener('click', function () {
            const itemId = this.dataset.itemId;

            // Fetch the item data from the server
            fetch(`/wishlist/api/items/${itemId}/`)
                .then(response => response.json())
                .then(data => {
                    // Populate the form fields
                    document.getElementById('editItemName').value = data.item_name;
                    document.getElementById('editItemDescription').value = data.description;
                    document.getElementById('editItemLink').value = data.link;
                    document.getElementById('editItemPriority').value = data.priority;

                    // Set the item ID on the form
                    document.getElementById('editItemForm').dataset.itemId = itemId;

                    // Show the modal
                    const editItemModal = new bootstrap.Modal(document.getElementById('editItemModal'));
                    editItemModal.show();
                })
                .catch(error => console.error('Error fetching item data:', error));
        });
    });

    // Edit Item Form Submission
    document.getElementById('editItemForm').addEventListener('submit', function (e) {
        e.preventDefault();
        const itemId = this.dataset.itemId;
        const formData = new FormData(this);
        const data = {
            item_name: formData.get('item_name'),
            description: formData.get('description'),
            link: formData.get('link'),
            priority: formData.get('priority'),
        };

        fetch(`/wishlist/api/items/${itemId}/`, {
            method: 'PUT',
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
                    $('#editItemModal').modal('hide');

                    // Refresh the page
                    window.location.reload();
                } else {
                    alert('Error: ' + JSON.stringify(data));
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error updating item: ' + error.message);
            });
    });

    // Delete Item: Show Modal
    document.querySelectorAll('.delete-item').forEach(button => {
        button.addEventListener('click', function () {
            const itemId = this.dataset.itemId;

            // Store the item ID in a global variable or data attribute
            document.getElementById('deleteItemModal').dataset.itemId = itemId;

            // Show the modal
            const deleteItemModal = new bootstrap.Modal(document.getElementById('deleteItemModal'));
            deleteItemModal.show();
        });
    });

    // Delete Item: Handle Confirmation
    document.getElementById('confirmDeleteItem').addEventListener('click', function () {
        const itemId = document.getElementById('deleteItemModal').dataset.itemId;

        if (itemId) {
            fetch(`/wishlist/api/items/${itemId}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                },
            })
                .then(response => {
                    if (response.ok) {
                        // Close the modal
                        const deleteItemModal = bootstrap.Modal.getInstance(document.getElementById('deleteItemModal'));
                        deleteItemModal.hide();

                        // Refresh the page
                        window.location.reload();
                    } else {
                        alert('Error deleting item.');
                    }
                })
                .catch(error => console.error('Error:', error));
        }
    });

    // Handle the "X" button and other modal closing events for the Delete Item Modal
    document.getElementById('deleteItemModal').addEventListener('hidden.bs.modal', function () {
        console.log('Delete Item Modal closed');
        // Remove the backdrop manually if it persists
        const backdrops = document.querySelectorAll('.modal-backdrop');
        backdrops.forEach(backdrop => backdrop.remove());
        // Optionally, clear the hidden input or reset the state
        document.getElementById('deleteItemModal').dataset.itemId = '';
    });
});