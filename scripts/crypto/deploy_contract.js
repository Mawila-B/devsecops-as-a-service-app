const hre = require("hardhat");

async function main() {
  const CryptoPayment = await hre.ethers.getContractFactory("CryptoPayment");
  const cryptoPayment = await CryptoPayment.deploy();
  
  await cryptoPayment.deployed();
  
  console.log("CryptoPayment deployed to:", cryptoPayment.address);
  
  // Verify contract on Etherscan
  await hre.run("verify:verify", {
    address: cryptoPayment.address,
    constructorArguments: [],
  });
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });