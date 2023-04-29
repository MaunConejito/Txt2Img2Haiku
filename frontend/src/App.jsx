import { createContext } from 'react';

import { ChakraBaseProvider, extendBaseTheme } from '@chakra-ui/react';
import chakraTheme from '@chakra-ui/theme';

import HaikuSearch from './components/HaikuSearch.jsx';
import SidebarFrame from './components/SidebarFrame.jsx';

import { config } from './config.js';

const {
  SimpleGrid,
  Box,
  Center,
  Stack,
  Image,
  Spinner,
  InputGroup,
  Input,
  InputRightElement,
  Button,
  Text,
  Heading,
  Container,
  AspectRatio,
  Spacer
} = chakraTheme.components;
const theme = extendBaseTheme({
  components: {
    SimpleGrid,
    Box,
    Center,
    Stack,
    Image,
    Spinner,
    InputGroup,
    Input,
    InputRightElement,
    Button,
    Text,
    Heading,
    Container,
    AspectRatio,
    Spacer
  },
});

export const ConfigContext = createContext(config);

export default function App() {
  return (
    <ConfigContext.Provider value={config}>
      <ChakraBaseProvider theme={theme}>
        <SidebarFrame>
          <HaikuSearch/>
        </SidebarFrame>
      </ChakraBaseProvider>
    </ConfigContext.Provider>
  );
}
