function loadCustomers(){

fetch("/api/customers")
.then(res=>res.json())
.then(data=>{

customerTable.innerHTML="";

data.forEach(c=>{
customerTable.innerHTML+=`
<tr>
<td>${c.name}</td>
<td>${c.whatsapp}</td>
<td>${c.city}</td>
<td><span class="badge bg-success">${c.status}</span></td>
<td>${c.inquiries}</td>
<td>${c.budget}</td>
<td>${c.area}</td>
</tr>
`;
});

});
}
