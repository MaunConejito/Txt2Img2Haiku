import { createContext } from 'react';

import { ChakraBaseProvider, extendBaseTheme } from '@chakra-ui/react';
import chakraTheme from '@chakra-ui/theme';

import HaikuSearch from './components/HaikuSearch.jsx';

import { config } from './config.js';

const { SimpleGrid, Box, Center, Stack, Image, Spinner, InputGroup,
        Input, InputRightElement, Button, Text, Container, AspectRatio } = chakraTheme.components;
const theme = extendBaseTheme({
  components: { SimpleGrid, Box, Center, Stack, Image, Spinner, InputGroup,
                Input, InputRightElement, Button, Text, Container, AspectRatio },
});

export const ConfigContext = createContext(config);

export default function App() {
  return (
    <ConfigContext.Provider value={config}>
      <ChakraBaseProvider theme={theme}>
        <HaikuSearch/>
      </ChakraBaseProvider>
    </ConfigContext.Provider>
  );
}
