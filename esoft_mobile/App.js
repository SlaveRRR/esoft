import React, { useState, useEffect, useCallback } from 'react';
import { View, Text, Button, TextInput, StyleSheet, ActivityIndicator, FlatList, TouchableOpacity, Alert  } from 'react-native';
import { NavigationContainer, useFocusEffect  } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Registration Screen Component
function RegisterScreen({ navigation }) {
  const [name, setName] = React.useState('');
  const [password, setPassword] = React.useState('');

  const storeRegistration = async (value1,value2) => {
    try {
      await AsyncStorage.setItem('token', value1);
      await AsyncStorage.setItem('user', value2);
    } catch (e) {
      console.log("Мдда пришла")
    }
  };

  const handleRegister = async () => {
    const url = "https://2b4b-95-181-208-83.ngrok-free.app/api/registrate";

// Данные для отправки
    let data = {
      nickname: name,
      password: password,
    };

// Опции запроса
  console.log("data",data)
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  };

// Выполнение запроса]
  console.log("response")
  let res = await fetch(url, options)
  console.log("res",res)
  let result = await res.json(); 
  console.log(result,"result")
    console.log(result.token,"token")
    console.log(typeof result.user.toString())
    storeRegistration(result.token,result.user.toString())
    if(result){
      navigation.navigate('Home',{params:result});
    }
       // Navigate to the HomeScreen after registration
    
    
  };


  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
      <Text>Registration Screen</Text>
      <TextInput
        placeholder="Name"
        value={name}
        onChangeText={setName}
        style={{ height: 40, borderColor: 'gray', borderWidth: 1, marginBottom: 10, paddingHorizontal: 8 }}
      />
      <TextInput
        placeholder="Password"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
        style={{ height: 40, borderColor: 'gray', borderWidth: 1, marginBottom: 10, paddingHorizontal: 8 }}
      />
      <Button title="Register" onPress={handleRegister} />
    </View>
  );
}

const HomeScreen = ({ route, navigation }) => {
  const { params } = route.params;
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchData = useCallback(async () => {
    try {
      const response = await getEvents(params.user);
      setEvents(response.events);
    } catch (error) {
      console.error('Error fetching events:', error);
    } finally {
      setLoading(false);
    }
  }, [params]);

  useEffect(() => {
    if (params && params.user) {
      fetchData();
    }
  }, [params, fetchData]);

  useFocusEffect(
    useCallback(() => {
      fetchData();
    }, [fetchData])
  );

  const getEvents = async (id) => {
    const url = "https://2b4b-95-181-208-83.ngrok-free.app/api/get_events";

    let data = {
      user: id,
    };

    const options = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    };

    let res = await fetch(url, options);
    let result = await res.json();

    if (result) {
      console.log("result", result);
      return result;
    }
  };

  const handleDeleteEvent = async (id) => {
    try {
      // Отправляем запрос на удаление события по его id
      const url = `https://2b4b-95-181-208-83.ngrok-free.app/api/delete_event`;
      let datas = {
        id: id,
      };
      const options = {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(datas),
      };
      await fetch(url, options);

      const updatedEvents = events.filter((event) => event.id !== id);
      setEvents(updatedEvents);

      Alert.alert('Success', 'Event deleted successfully');
    } catch (error) {
      console.error('Error deleting event:', error);
      Alert.alert('Error', 'Failed to delete event');
    }
  };

  const handleAddSchedule = () => {
    navigation.navigate('AddSchedule',{params:params});
  };

  if (loading) {
    return (
      <View style={styles.container}>
        <ActivityIndicator size="large" color="#0000ff" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <TouchableOpacity style={styles.addButton} onPress={handleAddSchedule}>
          <Text style={{ color: '#000', fontSize: 18 }}>Добавить расписание</Text>
      </TouchableOpacity>
      {events.length > 0 ? (
        <FlatList
          data={events}
          keyExtractor={(item) => item.id.toString()}
          renderItem={({ item }) => (
            <View style={styles.eventContainer}>
              <Text style={styles.eventText}>
                Comment: {item.comment}
              </Text>
              <Text style={styles.eventText}>
                Event Length: {item.event_length}
              </Text>
              <Text style={styles.eventText}>
                Event Take: {item.event_take}
              </Text>
              <Text style={styles.eventText}>
                Event Type: {item.event_type.name}
              </Text>
              <TouchableOpacity onPress={() => handleDeleteEvent(item.id)}>
                <Text style={{ color: 'red', marginTop: 8 }}>Delete Event</Text>
              </TouchableOpacity>
            </View>
          )}
        />
        
      ) : (
        <Text>No events available</Text>
      )}
      <TouchableOpacity style={styles.addButton} onPress={handleAddSchedule}>
        <Text style={{ color: '#fff', fontSize: 18 }}>Добавить расписание</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#fff',
  },
  eventContainer: {
    marginBottom: 16,
    borderWidth: 1,
    borderColor: '#ddd',
    padding: 16,
  },
  eventText: {
    fontSize: 16,
    marginBottom: 8,
  },
});

const AddSchedule = ({ route, navigation }) => {
  const { params } = route.params;
  console.log(route.params.params.user,"route.params")
  const [eventTake, setEventTake] = useState('');
  const [eventLength, setEventLength] = useState('00:00:00');
  const [eventType, setEventType] = useState(1);
  const [comment, setComment] = useState('Комментарий отсутствует');

  const handleCreateEvent = async () => {
    const url = 'https://2b4b-95-181-208-83.ngrok-free.app/api/create_event';
    console.log(route.params.params.user,"route.params.params.user")
    const data = {
      event_take: eventTake,
      event_length: eventLength,
      event_type: eventType,
      comment: comment,
      user: route.params.params.user,
    };
    console.log("data",data)
    const options = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    };

    try {
      const response = await fetch(url, options);
      const result = await response.json();
      
      console.log('Event created successfully:', result);
      navigation.navigate('Home',{params:params});
    } catch (error) {
      console.error('Error creating event:', error);
    }
  };

  return (
    <View style={style.container}>
      <Text>Добавить расписание</Text>
      <TextInput
        placeholder="Дата и время"
        value={eventTake}
        onChangeText={(text) => setEventTake(text)}
        style={style.input}
      />
      <TextInput
        placeholder="Продолжительность"
        value={eventLength}
        onChangeText={(text) => setEventLength(text)}
        style={style.input}
      />
      <TextInput
        placeholder="Тип события"
        value={eventType}
        onChangeText={(text) => setEventType(text)}
        style={style.input}
      />
      <TextInput
        placeholder="Комментарий"
        value={comment}
        onChangeText={(text) => setComment(text)}
        style={style.input}
      />
      <Button title="Создать событие" onPress={handleCreateEvent} />
    </View>
  );
};


const style = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  input: {
    height: 40,
    borderColor: 'gray',
    borderWidth: 1,
    marginBottom: 10,
    width: '80%',
    paddingHorizontal: 10,
  },
});

const Stack = createNativeStackNavigator();

function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="SignIn">
        <Stack.Screen name="SignIn" component={RegisterScreen} />
        <Stack.Screen name="AddSchedule" component={AddSchedule} />
        <Stack.Screen name="Home" component={HomeScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

export default App;

// import DetailsScreen from './app/Details.js';
// <Stack.Screen name="Details" component={DetailsScreen} />

// const HomeScreen = ({ route, navigation }) => {
//   const { params } = route.params
  
//   const getEvents = async (id) => {
//     const url = "https://c77b-95-181-208-83.ngrok-free.app/api/get_events";
  
//     // Данные для отправки
//     let data = {
//       user: id,
//     };
  
//   // Опции запроса
//     console.log("data",data)
//     const options = {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//       },
//       body: JSON.stringify(data),
//     };
  
//     let res = await fetch(url, options).catch(function(error) {
//       console.log('There has been a problem with your fetch operation: ' + error.message);
//       throw error;
//     });
//     let result = await res.json();
//     if(result){
//       console.log("result",result)
//     return result
//     }
//   }
//   events = getEvents(params.user)
//   console.log("eventsAAAAAAAAAAAAAAAAa")
//   console.log("events",events)
  
//   return (
//     <View>
//       <Text>Home {JSON.stringify(params)}</Text>
//       <Text>EVENTS {JSON.stringify(events)}</Text>
//     </View>
//   )
//   };