import { useState, useEffect, useReducer } from 'react';
import { arraysEqual } from '../utils.js';

import { InputGroup, Input, InputRightElement, Center, Box, Button } from '@chakra-ui/react'

import HaikuFinder from './HaikuFinder.jsx';
import QueryBuilder from './QueryBuilder.jsx';
import VerticalLine from './VerticalLine.jsx';

function queryObjectReducer(current, action) {
  switch(action.type) {
    case 'setQueryObject':
      return action.payload;
    case 'removeText':
      return {
        ...current,
        texts: current.texts.filter((t) => t !== action.payload)
      }
    case 'emptyTexts':
      return {
        ...current,
        texts: []
      }
    case 'setVectors':
      return {
        ...current,
        vectors: action.payload
      }
    case 'addVector':
      return {
        ...current,
        vectors: [
          ...current.vectors,
          action.payload
        ]
      }
    case 'removeVector':
      return {
        ...current,
        vectors: current.vectors.filter(
          (v) => !arraysEqual(v, action.payload)
        )
      }
    default:
      return current;
  }
}

export default function HaikuSearch() {
  const [inputValue, setInputValue] = useState('');
  const [queryText, setQueryText] = useState(null);
  const [queryObject, queryObjectDispatch] = useReducer(queryObjectReducer, null)

  const onInputChange = (e) => {
    setInputValue(e.target.value);
  }

  const onSubmit = (e) => {
    setQueryText(inputValue);
    queryObjectDispatch({
      type: 'setQueryObject',
      payload: inputValue ? {
        texts: [ inputValue ]
      } : null
    });
  }

  const onKeyUp = (e) => {
    if(e.key == 'Enter'){
      onSubmit(e)
    }
  }

  return (
    <Box
    p='20px'>
      <Center>
        <InputGroup
        onSubmit={onSubmit}>
          <Input
          placeholder='Enter search query ...'
          onChange={onInputChange}
          onKeyUp={onKeyUp}/>
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
        {queryText && <>
          <VerticalLine/>
          <QueryBuilder
          queryText={queryText}
          queryDispatch={queryObjectDispatch}
          n={9}/>
        </>}
        {queryObject && <>
          <VerticalLine/>
          <HaikuFinder
          query={queryObject}
          n={4}/>
        </>}
      </Box>
    </Box>
  );
}
