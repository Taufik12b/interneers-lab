// Example: Fetch product with ID = 1 from Django
const productApiUrl = "http://127.0.0.1:8001/products/";

fetch(productApiUrl)
  .then(response => {
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return response.json();
  })
  .then(product => {
    console.log("Product from Django:", product);
    
    document.getElementById("product-image").src = product.image || "image-app.png"; // fallback
    document.getElementById("product-title").textContent = product.name || "No title";
    document.getElementById("product-description").textContent = product.description || "No description";
    document.getElementById("product-price").textContent = `$${product.price || "0.00"}`;
  })
  .catch(error => {
    console.error("Failed to load product:", error);
  });
