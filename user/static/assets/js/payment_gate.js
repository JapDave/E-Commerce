const serverUrl = "https://c4pw4y29hyb6.usemoralis.com:2053/server";
const appId = "bj5sabPupSSvRDmtft9CH5cy8oVGC5pcP8XcGFFC";
Moralis.start({ serverUrl, appId });
const CONTRACT_ADDRESS = '0x9cb81bBE04741ee559D684EC36B44b6B1c4d01CB';



async function get_current_usd (url) {
  let response = await fetch(url);
  let data = await response.json();
  return data.conversion_result;
}


async function render(amount){
  var url = "https://v6.exchangerate-api.com/v6/c3ed988fb75118f140adda52/pair/INR/USD/"+amount;
  var Usd = await get_current_usd(url);
  console.log(Usd)
  var ethPrice =  await contract.methods.getPrice().call({from: ethereum.selectedAddress})/10**18;
  console.log(ethPrice);
  var resultedAmount = Usd/ethPrice*10**18;
  console.log(resultedAmount);
  await contract.methods.fund().send({value:resultedAmount,from: ethereum.selectedAddress})
  .then(function(){
    document.forms['main_form'].submit();
    
  })
  .catch(function (error){
    alert("Order Failed To Purchased");
  });

}



async function init(amount) {
   window.web3 = await Moralis.enableWeb3();
   window.contract = new web3.eth.Contract(contractAbi, CONTRACT_ADDRESS);
   user = await Moralis.User.current();
   if (user) {
      console.log(user);
      render(amount);
   }
   else {
      user = await Moralis.authenticate({ signingMessage: "Log in using Moralis" })
      render(amount);
      
   }
 }

