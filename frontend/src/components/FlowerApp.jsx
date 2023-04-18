import { useState, useEffect } from 'react';

import { InputGroup, Input, InputRightElement, Center, Box, Button } from '@chakra-ui/react'

import ImgDisplay from './ImgDisplay.jsx';


export default function FlowerApp({ config }) {
  const [inputValue, setInputValue] = useState('');
  const [imgs, setImgs] = useState([]);
  const [ready, setReady] = useState(true);

  const extractImgList = (resultJson) => {
    return resultJson.results.map((r) => r.payload.fileName);
  };

  const fetchImgs = async (q, n) => {
    setReady(false);
    fetch(config.serviceUrl +
          '/api/flowers/search?q=' + q + '&n=' + n)
      .then((response) => response.json())
      .then((json) => {
        setImgs(extractImgList(json));
        setReady(true);
      });
  };

  const onInputChange = (e) => {
    setInputValue(e.target.value);
  }

  const onSubmit = (e) => {
    fetchImgs(inputValue, 50);
  }

  return (
    <Box>
      <Center>
        <InputGroup
        m='20px'
        onSubmit={onSubmit}>
          <Input
          placeholder='How do you want your bouquet to be?'
          onChange={onInputChange}/>
          <InputRightElement
          width='4rem'>
            <Button w='3rem' h='1.75rem'
            size='sm'
            onClick={onSubmit}>
              go
            </Button>
          </InputRightElement>
        </InputGroup>
      </Center>
      <Box>
        <ImgDisplay imgs={imgs} waiting={!ready}/>
      </Box>
    </Box>
  );
}
