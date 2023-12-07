import AsyncStorage from '@react-native-async-storage/async-storage';

const storeData = async (value) => {
    try {
      await AsyncStorage.setItem('my-key', value);
    } catch (e) {
      // saving error
    }
  };

const getData = async () => {
    try {
      const value = await AsyncStorage.getItem('my-key');
      if (value !== null) {
        // value previously stored
      }
    } catch (e) {
      // error reading value
    }
  };

export default storage;