
  document.getElementById("backToNavbar").addEventListener("click", function () {
    // Close the offcanvas Home
    var offcanvasHome = document.getElementById("offcanvasHome");
    var bsOffcanvasHome = bootstrap.Offcanvas.getInstance(offcanvasHome);
    bsOffcanvasHome.hide();
  
    // Open the offcanvas Navbar after Home is closed
    var offcanvasNavbar = document.getElementById("offcanvasNavbar");
    var bsOffcanvasNavbar = new bootstrap.Offcanvas(offcanvasNavbar);
    bsOffcanvasNavbar.show();
  });
  
  