from abc import ABC, abstractmethod


class UserBaseService(ABC):

    @abstractmethod
    def register(self):
        """ 
        Abstract method to register users.
        """
        pass

    @abstractmethod
    def verify_otp(self):
        """ 
        Abstract method to verify user email.
        """
        pass