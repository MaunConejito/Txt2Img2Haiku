import React, { ReactNode, useEffect } from 'react';
import {
  IconButton,
  Box,
  Stack,
  CloseButton,
  Flex,
  Link,
  Image,
  useBreakpointValue,
  Drawer,
  DrawerContent,
  Text,
  Heading,
  useDisclosure
} from '@chakra-ui/react';
import {
  QuestionOutlineIcon,
  ExternalLinkIcon
} from '@chakra-ui/icons'

export default function SidebarFrame({ children }: { children: ReactNode }) {
  const { isOpen, onOpen, onClose } = useDisclosure();

  // automatic close on breakpont change
  // to prevent unclosed invisible drawer from blocking content
  const breakpoint = useBreakpointValue({ base: 'base', md: 'md'});
  useEffect(onClose, [onClose, breakpoint])

  return (
    <Box minH='100vh' bg='gray.100'>
      <SidebarContent
        onClose={onClose}
        display={{ base: 'none', md: 'block' }}
      />
      <Drawer
        autoFocus={false}
        isOpen={isOpen}
        placement='left'
        onClose={onClose}
        returnFocusOnClose={false}
        onOverlayClick={onClose}
        size='full'>
        <DrawerContent>
          <SidebarContent onClose={onClose}/>
        </DrawerContent>
      </Drawer>
      <MobileNav display={{ base: 'flex', md: 'none' }} onOpen={onOpen} />
      <Box ml={{ base: 0, md: 60 }} p='4'>
        {children}
      </Box>
    </Box>
  );
}

const Logo = ({ spacing, ...rest }) => (
  <Stack
    direction='row'
    spacing={spacing}
    align='center'
    {...rest}>
    <Image src='/logo.png' maxW='12'/>
    <Text fontSize='xl'
    fontFamily='monospace'
    fontWeight='bold'>
      Txt2Img2Haiku
    </Text>
  </Stack>
)

const InfoText = ({ ...rest }) => (
  <Stack
    direction='column'
    p='4'
    style={{overflow: 'auto'}}
    {...rest}>
    <Heading as='h2' size='md'>
      1. Enter Query
    </Heading>
    <Text align='justify' pl='2'>
      {'Enter a text that describes a general topic of '}
      <em>Haiku</em>
      {' you want to find.'}
    </Text>
    <Text align='justify' pl='2'>
      {'Try for example \'nature\' or \'city\'.'}
    </Text>
    <Heading as='h2' size='md' pt='2'>
      2. Refine Query
    </Heading>
    <Text align='justify' pl='2'>
      {'If you want, you can '}
      <em>refine</em>
      {' your search query using images.'}
    </Text>
    <Text align='justify' pl='2'>
      {'Just select one or multiple'}
      {' images that fit the mood you have in mind.'}
    </Text>
    <Heading as='h2' size='md' pt='2'>
      3. Get Results
    </Heading>
    <Text align='justify' pl='2'>
      {'The app will display the six '}
      <em>Haiku</em>
      {' from the database that best fit all selected images'}
      {' (or your original query if you did not refine it).'}
    </Text>
  </Stack>
)

const SidebarContent = ({ onClose, ...rest }) => {
  return (
    <Box
      bg={'white'}
      borderRight={'1px'}
      borderRightColor={'gray.200'}
      w={{ base: 'full', md: 60 }}
      pos='fixed'
      h='full'
      {...rest}>
      <Flex
        h='20'
        alignItems='center'
        mx='4'
        justifyContent='space-between'
        borderBottom={'1px'}
        borderBottomColor={'gray.200'}>
        <Logo spacing={{ base: '4', md: '2' }}/>
        <CloseButton display={{ base: 'flex', md: 'none' }} onClick={onClose} />
      </Flex>
      <InfoText
        position='absolute'
        top={20}
        bottom={10}/>
      <Flex
        alignItems='center'
        justify='center'
        position='absolute'
        bottom={0}
        h={10}
        w={{ base: 'calc(100% - 30px)', md: '52' }}
        mx='4'
        borderTop={'1px'}
        borderTopColor={'gray.200'}>
        <Link fontSize='sm' href='https://github.com/FatMadLad/Txt2Img2Haiku' isExternal>
          GitHub Repository <ExternalLinkIcon mx='2px' />
        </Link>
      </Flex>
    </Box>
  );
};

const MobileNav = ({ onOpen, ...rest }) => {
  return (
    <Flex
      ml={{ base: 0, md: 60 }}
      px={{ base: 4, md: 24 }}
      height='20'
      alignItems='center'
      bg='white'
      borderBottomWidth='1px'
      borderBottomColor='gray.200'
      justifyContent='flex-start'
      {...rest}>
      <IconButton
        variant='outline'
        onClick={onOpen}
        aria-label='open menu'
        icon={<QuestionOutlineIcon boxSize={5}/>}
      />
      <Logo ml='8' spacing='4'/>
    </Flex>
  );
};
