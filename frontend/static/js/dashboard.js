function loadPage(url){
fetch(url)
.then(res => res.text())
.then(html => {
document.getElementById("content-area").innerHTML = html;

// AUTO LOAD PROPERTY DATA
if(url.includes("properties")){
  if(typeof loadData === "function"){
     loadData();
  }
}

});
}

// Default
loadPage("/admin/dashboard");

function toggleSidebar(){
document.getElementById("sidebar").classList.toggle("d-none");
}

if(url.includes("customers")){
   if(typeof loadCustomers === "function"){
      loadCustomers();
   }
}

if(url.includes("inquiries")){
   if(typeof loadInquiries === "function"){
      loadInquiries();
   }
}

