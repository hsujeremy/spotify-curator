import styled from 'styled-components'
import { Colors } from '../../styles/index'

export const Container = styled.div`
  width: 100%;
  min-height: 100vh;
  background: ${Colors.primary};
  display: flex;
  justify-content: center;

`
export const ContainerInner = styled.div`
  width: 100%;
  max-width: 1024px;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;

`

export const Form = styled.div`
  width: 80%;
  max-width: 400px;

  h1 {
    color: #ffffff;
  }
`

export const Row = styled.div`
  width: 100%;
  display: flex;
  justify-content: space-between;
`

export const Icon = styled.div`
  color: ${Colors.ternary};
  &:hover {
    ${Colors.hightlight};
    cursor: pointer;
  }
`

export const Input = styled.input`
  width: 86%;
    -webkit-box-sizing: border-box; /* Safari/Chrome, other WebKit */
    -moz-box-sizing: border-box;    /* Firefox, other Gecko */
    box-sizing: border-box;
  margin-bottom: 1em;
  font-family: 'Roboto', sans-serif;

  background-color: ${Colors.secondary};
  padding: 0.5rem 0rem 0.5rem 1rem;
  font-size: 0.9rem;
  font-weight: 400;
  line-height: 1.5;
  color: #ffffff;
  transition: 0.2s;
  box-shadow: none;
  border: 1px solid #ffffff;
  border-radius: 0.25rem;
  font-family: 'Inter', sans-serif;


  &:focus {
    outline: 0;
    border-color: ${Colors.hightlight};
    box-shadow: 0 0 1.25rem rgba(31, 45, 61, 0.08);
  }
`;

export const Button = styled.button`
  width: 100%;
  font-family: 'Roboto', sans-serif;

  padding: 8px 20px;
  border-radius: 25px;
  // background-color: ${Colors.hightlight};
  background: none;
  border: none;
  color: #ffffff;
  box-shadow: 0 2px 0 rgba(0,0,0,.045);
  height: 40px;
  font-weight: 600;
  margin-bottom: 1.5em;
  border: 1px solid #ffffff;
  transition: 0.2s;

  &:hover {
    background-color: ${Colors.hightlight};
    border: 1px solid ${Colors.hightlight};
    cursor: pointer;
  }
`;

export const Add = styled.div`
  -webkit-box-sizing: border-box; /* Safari/Chrome, other WebKit */
  -moz-box-sizing: border-box;    /* Firefox, other Gecko */
  box-sizing: border-box;
  width: 100%;
  display: flex;
  margin-bottom: 1.5em;
  align-items: center;
  transition: 0.2s;
  border-radius: 5px;
  padding: 5px 10px 5px 10px;

  &:hover{
    background: ${Colors.secondary};
    cursor: pointer;
  }
`

export const AddButton = styled.p`
  margin: 0 0 0 10px;
  color: ${Colors.ternary};
`
