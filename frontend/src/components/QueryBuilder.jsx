import { useState, useEffect, useContext } from 'react';

import { SimpleGrid, Box, Center, AspectRatio, Container,
         Image, Spinner, Circle, Button, Collapse, useDisclosure } from '@chakra-ui/react'
import { ChevronDownIcon, ChevronUpIcon } from '@chakra-ui/icons'


import { ConfigContext } from '../App.jsx';
import ImgDisplay from './ImgDisplay.jsx';


const fcolor = '#dd6644'

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
    setSelected((s) => s.map((b, j) => j==i ? !b : b));
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
  }, [queryText])

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
  }, [selected, vectors]);

  return (
    <Container
    maxW='xl'
    p='0px'
    position='relative'
    minH='40px'
    border='10px'
    >
      <Center>
        <Button
        onClick={onToggle}
        position='absolute'
        top={0}
        zIndex={2}
        border='2px'
        borderColor={selected.some((b) => b) ?
          fcolor : 'gray.300'}
        borderRadius='full'
        boxShadow={selected.some((b) => b) ?
          '0px 0px 0px 2px ' + fcolor :
          null}>
          Refine your query
          {isOpen ?
            <ChevronUpIcon
            boxSize={8}/> :
            <ChevronDownIcon
            boxSize={8}/>}
        </Button>
      </Center>
      <Collapse in={isOpen} animateOpacity>
        <Box
        centerContent
        mt='18px'
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
                  boxShadow={selected[i] ?
                    '0px 0px 0px 4px ' + fcolor :
                    null}
                  _hover={{
                    boxShadow: 'outline'
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
    </Container>
  );
}
