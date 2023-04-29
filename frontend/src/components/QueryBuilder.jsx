import { useState, useEffect, useContext } from 'react';

import { SimpleGrid, Box, Center, Container,
         Image, Spinner, Button, Collapse, useDisclosure } from '@chakra-ui/react'
import { ChevronDownIcon, ChevronUpIcon } from '@chakra-ui/icons'


import { ConfigContext } from '../App.jsx';


export default function QueryBuilder({ queryText, queryDispatch, n }) {
  const { isOpen, onToggle } = useDisclosure();
  const config = useContext(ConfigContext);
  const [urls, setUrls] = useState(null);
  const [vectors, setVectors] = useState([]);
  const [selected, setSelected] = useState(new Array(n).fill(false));

  const extractUrlList = (resultJson) => {
    return resultJson.results.map((r) => r.payload.url);
  };
  const extractVectorList = (resultJson) => {
    return resultJson.results.map((r) => r.vector);
  };

  const toggleSelected = (i) => {
    setSelected((s) => s.map((b, j) => j===i ? !b : b));
  }

  useEffect(() => {
    setSelected(new Array(n).fill(false));
    setUrls(null);
    fetch(config.serviceUrl + '/api/imgs/search?q='
                            + queryText + '&n=' + n)
    .then((response) => response.json())
      .then((json) => {
        setUrls(extractUrlList(json));
        setVectors(extractVectorList(json));
      });
  }, [queryText, config.serviceUrl, n])

  useEffect(() => {
    if (selected.some((b) => b)) {
      queryDispatch({
        type: 'setQueryObject',
        payload: {
          vectors: vectors.filter((_, i) => selected[i])
        }
      });
    } else {
      queryDispatch({
        type: 'setQueryObject',
        payload: {
          texts: [ queryText ]
        }
      });
    }
  }, [selected, vectors, queryDispatch, queryText]);

  const selectedColor = '#dd6644'
  const focusColor = '#88bbff'
  const selectedFocusColor = '#eeaa44'

  const imgBoxShadow = (selected, hover) => {
    const color = selected && hover ? selectedFocusColor : (
      selected ? selectedColor : (
        hover ? focusColor : ''
      )
    )
    return selected || hover ? '0px 0px 0px 3px ' + color : null;
  }

  return (
    <Container
    maxW='xl'
    p='0px'
    pt='18px'
    position='relative'
    minH='40px'
    >
      <Collapse in={isOpen}
      style={{overflow: 'visible'}}>
        <Box
        centerContent
        pt='18px'
        border='2px'
        borderColor='gray.300'
        bg='gray.50'
        borderRadius='20px'
        boxShadow='md'>
          {urls ? (
            <SimpleGrid
            columns={3}>
              {urls.map((url, i) =>
                <Center
                m='10px'
                key={i}>
                  <Image
                  onClick={() => toggleSelected(i)}
                  src={url}
                  fallbackSrc={'/no_image.png'}
                  key={i}
                  fit='contain'
                  borderRadius='10'
                  boxShadow={imgBoxShadow(selected[i], false)}
                  _hover={{
                    boxShadow: imgBoxShadow(selected[i], true)
                  }}/>
                </Center>
              )}
            </SimpleGrid>
          ) : (
            <Center>
              <Spinner
              size='xl'
              m='20px'/>
            </Center>
          )}
        </Box>
      </Collapse>
      <Center>
        <Button
        onClick={onToggle}
        position='absolute'
        top="0px"
        border='2px'
        borderColor={selected.some((b) => b) ?
          selectedColor : 'gray.300'}
        borderRadius='full'
        boxShadow={selected.some((b) => b) ?
          '0px 0px 0px 1px ' + selectedColor :
          null}>
          Refine your query
          {isOpen ?
            <ChevronUpIcon
            boxSize={8}/> :
            <ChevronDownIcon
            boxSize={8}/>}
        </Button>
      </Center>
    </Container>
  );
}
