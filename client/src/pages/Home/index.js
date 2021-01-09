import React, { useState } from 'react'
import { Container, ContainerInner, Form, Input, Button, Add, AddButton, Row, Icon } from './styles'
import { IoAdd } from 'react-icons/io5'
import { IoMdTrash } from 'react-icons/io' 
import { IconContext } from "react-icons";
import { Colors } from '../../styles/index'
const Home = () => {
    const [song, songInput] = useState([''])
    const [inputs, addInputs] = useState([{}])

    const updateInput = (index, value) => {
        let newArr = [...song]
        newArr[index] = value
        songInput(newArr)
    }

    const addSong = () => {
        addInputs(inputs => [...inputs, {}])
        songInput(song => [...song, ''])
    }

    const deleteInput = (index) => {
        let newSong = [...song]
        let newInputs = [...inputs]

        newSong.splice(index, 1)
        newInputs.splice(index, 1)

        songInput(newSong)
        addInputs(newInputs)
    }

    return(
        <Container>
            <ContainerInner>
                <Form>
                    <h1>Find your preferences: </h1>
                    {inputs.map((component, index) => { 
                        return (
                            <Row key={index}>
                                <Input placeholder="Enter a song" 
                                       value={song[index]} 
                                       onChange={e => updateInput(index, e.target.value)}/>
                                <Icon onClick={() => deleteInput(index)}>
                                    <IconContext.Provider value={{ color: Colors.ternary, 
                                                        className: "global-class-name", 
                                                        style: { verticalAlign: 'middle' },
                                                        size: '2em' }}>
                                        <div>
                                            <IoMdTrash />
                                        </div>
                                    </IconContext.Provider>
                                </Icon>
                            </Row>
                            )
                    }) }
                    <Add onClick={() => addSong()}>
                        <IconContext.Provider value={{ color: Colors.ternary, 
                                                    className: "global-class-name", 
                                                    style: { verticalAlign: 'middle' },
                                                    size: '2em' }}>
                            <div>
                                <IoAdd />
                            </div>
                        </IconContext.Provider>
                        <AddButton>
                            Add Song
                        </AddButton>
                    </Add>
                    <Button>SUBMIT</Button>
                </Form>
            </ContainerInner>
        </Container>
    )
}

export default Home