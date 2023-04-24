import { useState, useEffect } from 'react';

import { InputGroup, Input, InputRightElement, Center, Box, Button } from '@chakra-ui/react'

import ImgDisplay from './ImgDisplay.jsx';
import HaikuDisplay from './HaikuDisplay.jsx';


export default function HaikuSearch({ config }) {
  const [inputValue, setInputValue] = useState('');
  const [urls, setUrls] = useState([]);
  const [urlsReady, setUrlsReady] = useState(true);
  const [haikus, setHaikus] = useState([]);
  const [haikusReady, setHaikusReady] = useState(true);

  const extractUrlList = (resultJson) => {
    return resultJson.results.map((r) => r.payload.url);
  };
  const extractHaikuList = (resultJson) => {
    return resultJson.results.map((r) => r.payload.lines);
  };

  const fetchUrls = async (q, n) => {
    setUrlsReady(false);
    fetch(config.serviceUrl +
          '/api/imgs/search?q=' + q + '&n=' + n)
      .then((response) => response.json())
      .then((json) => {
        setUrls(extractUrlList(json));
        setUrlsReady(true);
      });
  };

  const fetchHaikus = async (q, n) => {
    setHaikusReady(false);
    fetch(config.serviceUrl +
          '/api/haikus/search?q=' + q + '&n=' + n)
      .then((response) => response.json())
      .then((json) => {
        setHaikus(extractHaikuList(json));
        setHaikusReady(true);
      });
  };

  const onInputChange = (e) => {
    setInputValue(e.target.value);
  }

  const onSubmit = (e) => {
    fetchUrls(inputValue, 24);
    fetchHaikus(inputValue, 8);
  }

  return (
    <Box>
      <Center>
        <InputGroup
        m='20px'
        onSubmit={onSubmit}>
          <Input
          placeholder='Enter search query ...'
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
        <HaikuDisplay haikus={haikus} waiting={!haikusReady}/>
        <ImgDisplay urls={urls} waiting={!urlsReady}/>
      </Box>
    </Box>
  );
}
