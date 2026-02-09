console.log("PROPERTY JS LOADED");

let selectedId = null;

/* LOAD DATA */
function loadData(){
fetch("/api/properties")
.then(res=>res.json())
.then(data=>{

propertyTable.innerHTML="";

data.forEach(p=>{
propertyTable.innerHTML += `
<tr>
<td>${p.type}</td>
<td>${p.size}</td>
<td>${p.price}</td>
<td>${p.city}</td>
<td>${p.status}</td>
<td>
<button class="btn btn-warning btn-sm" onclick="editProperty('${p._id}')">Edit</button>
<button class="btn btn-danger btn-sm" onclick="del('${p._id}')">Delete</button>
</td>
</tr>
`;
});

});
}



/* SAVE OR UPDATE */
function saveProperty(){

let payload = {
type: typeInput.value,
size: sizeInput.value,
price: priceInput.value,
city: cityInput.value,
status: statusInput.value
};

if(!payload.type || !payload.size || !payload.price || !payload.city || !payload.status){
alert("All fields required");
return;
}

if(selectedId === null){

// ADD
fetch("/api/properties",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify(payload)
});

}else{

// UPDATE
fetch(`/api/properties/${selectedId}`,{
method:"PUT",
headers:{"Content-Type":"application/json"},
body:JSON.stringify(payload)
});

}

bootstrap.Modal.getInstance(propertyModal).hide();
clearForm();
loadData();
}

/* EDIT */
function editProperty(id){

selectedId = id;

fetch("/api/properties")
.then(res=>res.json())
.then(data=>{

let p = data.find(x=>x._id === id);

typeInput.value = p.type;
sizeInput.value = p.size;
priceInput.value = p.price;
cityInput.value = p.city;
statusInput.value = p.status;

new bootstrap.Modal(propertyModal).show();
});
}

/* DELETE */
function del(id){
if(confirm("Delete property?")){
fetch(`/api/properties/${id}`,{method:"DELETE"})
.then(()=>loadData());
}
}

/* CLEAR */
function clearForm(){
selectedId = null;
typeInput.value="";
sizeInput.value="";
priceInput.value="";
cityInput.value="";
priceInput.value="";
statusInput.value="";
}
