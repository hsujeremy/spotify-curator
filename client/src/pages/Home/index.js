import React, { useState } from 'react';
import { Container, ContainerInner, Form, Input, Button, Add, AddButton, Row, Icon } from './styles';
import { IoAdd, /* IoWatchOutline */ } from 'react-icons/io5';
import { IoMdTrash } from 'react-icons/io';
import { IconContext } from 'react-icons';
import { Colors } from '../../styles/index';
import axios from 'axios';


const Home = () => {
    const [songs, songInput] = useState(['']);
    const [inputs, addInputs] = useState([{}]);
    const [predictions, updatePredictions] = useState({})

    const updateInput = (index, value) => {
        let newArr = [...songs];
        newArr[index] = value;
        songInput(newArr);
    }

    const addSong = () => {
        addInputs(inputs => [...inputs, {}]);
        songInput(songs => [...songs, '']);
    }

    const deleteInput = index => {
        let newSong = [...songs];
        let newInputs = [...inputs];

        newSong.splice(index, 1);
        newInputs.splice(index, 1);

        songInput(newSong);
        addInputs(newInputs);
    }

    const predictProbabilties = async () => {
        const nonEmptySongs = songs.filter(song => song.length > 0);
        if (nonEmptySongs.length === 0) {
            console.log('Need to enter at least one song!');
            return;
        }
        const json = JSON.stringify({ 'songs': nonEmptySongs });

        let response;
        try {
            response = await axios.post('/make_predictions', json, {
                headers: { 'Content-Type': 'application/json' }
            });
        } catch(e) {
            console.log(e);
            return;
        }

        let taskId = response.data.task_id;

        const timer = setInterval(async () => {
            let result = await checkTaskStatus(taskId);

            if (result === undefined) {
                clearInterval(timer);
                return;
            }

            if (result.data !== 'PENDING') {
                clearInterval(timer);
                if (result.data === 'FAILURE') {
                    updatePredictions({ status: 'FAILED' });
                } else {
                    updatePredictions({ status: 'SUCCEEDED', songs: result.data });
                }
                return result.data
            }
        }, 1000);
    }

    const checkTaskStatus = async taskId => {
        try {
            const result = await axios.get('/check/' + taskId);
            return result;
        } catch(e) {
            console.log(e);
        }
    }

    if (Object.keys(predictions).length === 0) {
        return (
            <Container>
                <ContainerInner>
                    <Form>
                        <h1>Find your preferences: </h1>
                        {inputs.map((component, index) => {
                            return (
                                <Row key={index}>
                                    <Input placeholder='Enter a song'
                                           value={songs[index]}
                                           onChange={e => updateInput(index, e.target.value)}/>
                                    <Icon onClick={() => deleteInput(index)}>
                                        <IconContext.Provider value={{ color: Colors.ternary,
                                                            className: 'global-class-name',
                                                            style: { verticalAlign: 'middle' },
                                                            size: '2em' }}>
                                            <div>
                                                <IoMdTrash />
                                            </div>
                                        </IconContext.Provider>
                                    </Icon>
                                </Row>
                            );
                        })}
                        <Add onClick={() => addSong()}>
                            <IconContext.Provider value={{ color: Colors.ternary,
                                                        className: 'global-class-name',
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
                        <Button onClick={() => predictProbabilties()}>SUBMIT</Button>
                    </Form>
                </ContainerInner>
            </Container>
        );
    } else {
        console.log(predictions);
        return (
            <div>Done</div>
        );
    }
}

export default Home;
