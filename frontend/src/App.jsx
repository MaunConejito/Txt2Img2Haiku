import { ChakraBaseProvider, extendBaseTheme } from '@chakra-ui/react'
import chakraTheme from '@chakra-ui/theme'

import FlowerApp from './components/FlowerApp.jsx';

import { config } from './config.js';

const { SimpleGrid, Box, Center, Image, Spinner, InputGroup,
        Input, InputRightElement, Button } = chakraTheme.components;
const theme = extendBaseTheme({
  components: { SimpleGrid, Box, Center, Image, Spinner, InputGroup,
                Input, InputRightElement, Button },
});

export default function App() {
  return (
    <ChakraBaseProvider theme={theme}>
      <FlowerApp config={config}/>
    </ChakraBaseProvider>
  );
}
